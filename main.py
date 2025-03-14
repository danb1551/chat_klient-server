import socket
import threading
import os

SERVER_IP = "127.0.0.1"  # Změňte na IP serveru
SERVER_PORT = 12345
nick = ""
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Došlo k odpojení od serveru.")
            client.close()
            break

def send_messages():
    while True:
        global nick
        message = input("Zadej zprávu: ")
        if message == "/stop":
            client.close()
            break
        elif message == "/help":
            print("/stop pro ukončení aplikace.")
            print("/help pro tuto zprávu.")
            print("/list pro seznam všech klientů.")
            print("/clear pro vymazání všech zpráv(nevymaže na straně serveru).")
            print("/nick [jméno] zadej pro změnu jména.")

        elif message == "/list":
            client.send("/list".encode('utf-8'))

        elif message == "/clear":
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')

        elif "/nick" in message:
            message1 = message.split(' ')
            nick = message1[1]
            print(f"nick úspěšně změněn na {nick}")

        elif nick != "":
            message = "[" + nick + "] " + message
            client.send(message.encode('utf-8'))
            print("Zpráva byla odeslána.")
        else:
            client.send(message.encode('utf-8'))
            print("Zpráva byla odeslána.")

threading.Thread(target=receive_messages).start()
send_messages()