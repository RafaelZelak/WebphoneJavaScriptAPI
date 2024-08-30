# WebphoneJavaScriptAPI

## Visão Geral

**WebphoneJavaScriptAPI** é a continuação do projeto **DiscadorSipWeb**, que foi descontinuado devido a limitações técnicas encontradas com a biblioteca PJSUA2 Python em ambientes web. Este novo projeto oferece uma solução moderna e eficaz para a implementação de um webphone utilizando tecnologias baseadas em JavaScript.

## Objetivo

O objetivo do **WebphoneJavaScriptAPI** é fornecer uma interface de webphone robusta e funcional, utilizando uma API JavaScript para operar o webphone via WebSocket. O backend é gerenciado com Flask, garantindo uma integração fluida e eficiente entre o frontend e o servidor.

## Principais Características

- **Integração WebSocket:** Utiliza WebSocket para comunicação em tempo real entre o cliente e o servidor.
- **Uso de Flask:** Mantém o Flask no backend para gerenciar a lógica do servidor e interações com a API.
- **Interface Moderna:** Interface de usuário estilizada para uma experiência de uso aprimorada.

## Começando

Para começar a usar ou contribuir para o **WebphoneJavaScriptAPI**, siga as etapas abaixo:

### 1. Clonar o Repositório

```bash
git clone https://github.com/seuusuario/WebphoneJavaScriptAPI
````

### 2. Instalar Dependências
Instale as dependências listadas no arquivo requirements.txt:

```bash
pip install -r requirements.txt
````

### 3. Configurar o LDAP e Asterisk
O WebphoneJavaScriptAPI utiliza Flask para realizar a autenticação via LDAP e se conectar ao servidor Asterisk.

#### a) Autenticação LDAP
A tela de login (localizada em templates/login.html) realiza a autenticação via LDAP. No arquivo app.py, você precisará configurar as informações de conexão com o seu servidor LDAP:
```python
conn.search(search_base='DC=dominio,DC=dominio',
            search_filter=f'(sAMAccountName={username})',
            attributes=['cn', 'homePhone', 'telephoneNumber'])
````

search_base: Deve ser alterado para as configurações do seu servidor LDAP.
O campo telephoneNumber no LDAP é utilizado para armazenar o ramal do usuário, e o campo homePhone armazena o telefone residencial.
#### b) Conexão com o Asterisk
Para integrar o webphone com o Asterisk, utilize uma imagem do Issabel (baseada em Linux Red Hat). No seu código, conecte-se ao servidor Asterisk via SSH utilizando o pacote paramiko:
```python
def get_all_callerid():
    hostname = 'IpAsterisk'
    port = 22
    username = 'root'
    password = 'SenhaRoot'
    file_path = '/etc/asterisk/sip_additional.conf'
````
#### file_path: No caso do Issabel, o arquivo de configurações SIP adicional está localizado em /etc/asterisk/sip_additional.conf. Certifique-se de ajustar o caminho conforme a distribuição ou sistema utilizado.

### Dependências
As seguintes dependências são necessárias para o funcionamento do projeto:
```plaintext
Flask
ldap3
paramiko
````
Instale todas utilizando o comando pip:

```bash
pip install Flask ldap3 paramiko
````
