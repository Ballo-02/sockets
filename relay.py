import socket
import ssl
import _thread
from subprocess import run
import sys

def interact(cert, host, port, data=0):
    context = ssl.SSLContext() #Defaults to TLS 
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cert)
    with socket.create_connection((host, port)) as sock:
        #Create secure socket
        ssock=context.wrap_socket(sock, server_hostname=host)
        print(ssock.version())
        print(ssock.getpeercert())
        ssock.send(data.encode())
if __name__=="__main__":
    cert="./cert.pem"
    host=sys.argv[2]
    print(host)
    if (sys.argv[3]=="-p"):
        port=sys.argv[4]
        print(port)
        if (sys.argv[5]=="-c"):
            command=sys.argv[6]
            print(command)
            interact(cert, host, port, command)