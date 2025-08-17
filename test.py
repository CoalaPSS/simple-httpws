import socket

HOST = '127.0.0.1'  # Endereço IP local
PORT = 8080        # Porta do servidor

def send_request(request_data, request_name):
    """Envia uma requisição HTTP e imprime a resposta."""
    print(f"--- Tentando enviar a requisição: {request_name} ---")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Conecta ao servidor
            s.connect((HOST, PORT))
            
            # Envia a requisição
            s.sendall(request_data.encode('utf-8'))
            
            # Recebe a resposta do servidor
            response = s.recv(4096).decode('utf-8', errors='ignore')
            
            print(f"Resposta recebida para a requisição '{request_name}':")
            print("-" * 40)
            print(response)
            print("-" * 40)
            
        except ConnectionRefusedError:
            print(f"Erro: Conexão recusada. Certifique-se de que o servidor está rodando na porta {PORT}.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
    print("\n")

# # --- Requisição 1: HTTP 2.0 (um protocolo mais recente e binário) ---
# # A mensagem é de texto, então provavelmente o servidor vai interpretar como HTTP 1.0 ou dar um erro
# request_2_0 = "GET / HTTP/2.0\r\nHost: 127.0.0.1\r\n\r\n"
# send_request(request_2_0, "HTTP 2.0")


# --- Requisição 2: Método CONNECT ---
# Esse método é usado para tunelamento, como em proxies
request_connect = "CONNECT www.example.com:443 HTTP/1.1\r\nHost: www.example.com\r\n\r\n"
send_request(request_connect, "CONNECT")