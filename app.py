from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from ldap3 import Server, Connection, ALL_ATTRIBUTES
import paramiko
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Altere isso para uma chave secreta real

# Função de autenticação LDAP
def authenticate(username, password):
    domain = 'digitalup.intranet'
    server = Server(domain, get_info=ALL_ATTRIBUTES)
    user = f'{username}@{domain}'
    conn = Connection(server, user=user, password=password)

    try:
        if conn.bind():
            # Buscando o nome completo e telefone do usuário
            conn.search(search_base='DC=digitalup,DC=intranet',
                        search_filter=f'(sAMAccountName={username})',
                        attributes=['cn', 'homePhone', 'telephoneNumber'])

            if len(conn.entries) > 0:
                user_info = conn.entries[0]

                # Exibindo as informações retornadas para depuração
                print(user_info)

                full_name = user_info.cn.value if hasattr(user_info, 'cn') else None
                phone_number = user_info.homePhone[0] if hasattr(user_info, 'homePhone') and user_info.homePhone else None
                # Se não encontrar em homePhone, tentar com telephoneNumber
                if not phone_number:
                    phone_number = user_info.telephoneNumber[0] if hasattr(user_info, 'telephoneNumber') and user_info.telephoneNumber else None

                # Salvando as informações na sessão
                session['logged_in'] = True
                session['username'] = username
                session['full_name'] = full_name
                session['phone_number'] = phone_number

                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print(f"Erro de autenticação LDAP: {e}")
        return False
    finally:
        conn.unbind()

# Função para obter o secret do servidor
import paramiko
import re

def get_secret_for_phone_number(phone_number):
    hostname = '192.168.15.252'
    port = 22
    username = 'root'
    password = 'Dydf%hhffjk5s588ik2u@ud7aDF'
    file_path = '/etc/asterisk/sip_additional.conf'

    try:
        # Inicializa o cliente SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conecta ao servidor
        client.connect(hostname, port, username, password)

        # Executa o comando para ler o arquivo
        stdin, stdout, stderr = client.exec_command(f'cat {file_path}')
        file_content = stdout.read().decode()

        # Verifica se houve algum erro
        error_message = stderr.read().decode()
        if error_message:
            print(f"Erro ao ler o arquivo: {error_message}")
            return None

        # Processa o conteúdo do arquivo
        sections = re.split(r'\n(?=\[\d+\])', file_content)
        for section in sections:
            if f'dial=SIP/{phone_number}' in section:
                # Busca o valor da linha secret
                match = re.search(r'secret=([^ \n]+)', section)
                if match:
                    return match.group(1)  # Retorna apenas o valor do secret

        return None

    except paramiko.SSHException as e:
        print(f"Erro de SSH: {e}")
        return None
    except Exception as e:
        print(f"Erro: {e}")
        return None
    finally:
        # Fecha a conexão SSH, se estiver aberta
        client.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if authenticate(username, password):
            return redirect(url_for('home'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')

    return render_template('login.html')

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Exibindo nome completo e telefone do usuário na página inicial
    full_name = session.get('full_name', 'Usuário')
    phone_number = session.get('phone_number', 'Não disponível')

    # Obtendo o secret para o número de telefone
    secret = get_secret_for_phone_number(phone_number) if phone_number != 'Não disponível' else 'Não disponível'

    return render_template('index.html', full_name=full_name, phone_number=phone_number, secret=secret)

from flask import jsonify

@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    if not session.get('logged_in'):
        return jsonify({'error': 'Usuário não autenticado'}), 401

    phone_number = session.get('phone_number', 'Não disponível')
    secret = get_secret_for_phone_number(phone_number) if phone_number != 'Não disponível' else 'Não disponível'

    return jsonify({
        'phone_number': phone_number,
        'secret': secret
    })


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('full_name', None)
    session.pop('phone_number', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
