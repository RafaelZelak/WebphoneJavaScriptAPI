
window.onload = function() {
    if (typeof webphone_api !== 'undefined') {
        webphone_api.onAppStateChange(function (state) {
            if (state === 'loaded') {
                // Defina os parâmetros necessários
                webphone_api.setparameter('serveraddress', '192.168.15.252'); // IP do servidor SIP
                webphone_api.setparameter('username', phoneNumber); // Nome de usuário SIP
                webphone_api.setparameter('password', secret); // Senha do usuário SIP

                // Inicie o webphone
                webphone_api.start();
            }
        });

        function makeCall() {
            var number = prompt("Enter the number to call:");
            if (number) {
                webphone_api.call(number);
            }
        }

        function hangUp() {
            webphone_api.hangup();
        }

        function sendMessage() {
            var number = prompt("Enter the recipient number:");
            var message = prompt("Enter your message:");
            if (number && message) {
                webphone_api.sendchat(number, message);
            }
        }
    } else {
        console.error('webphone_api is not defined');
    }
}