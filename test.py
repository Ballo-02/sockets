import socket
import ssl
import _thread
from subprocess import run
import sys
# def interact2(cert, key, host, port, data=0):
#     context = ssl.SSLContext() #Defaults to TLS 
#     context.verify_mode = ssl.CERT_REQUIRED
#     context.load_verify_locations(cert)
#     with socket.create_connection((host, port)) as sock:
#         #Create secure socket
#         ssock=context.wrap_socket(sock, server_hostname=host)
#         print(ssock.version())
#         print(ssock.getpeercert())
#         ssock.send(data)
    
# def interact(cert, key, host, port, data=0):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
#         sock.bind((host, port))
#         sock.listen(5)
#         with context.wrap_socket(sock, server_side=True) as ssock:
#             while 1:
#                 conn, addr = ssock.accept()
#                 print('Connected by', addr)
#                 while 1:
#                     recieve = conn.recv(1024)
#                     if (recieve  !=0):
#                         break
#                     print(f"Recieved: {recieve}")
#                 recieve=recieve.decode()
#                 command_split=recieve.split(" ")
#                 if (command_split[0]=="relay"):
#                     host=command_split[1]
#                     port=int(command_split[2])
#                     command=command_split[3]
# #                    _thread.start_new_thread(interact,(cert, key, host, port, command))
#                     conn.close()
#                     interact2(cert, key, host, port, command)
#                 else:
#                     command = run(command_split, capture_output=True).stdout
#                     conn.send(command)
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