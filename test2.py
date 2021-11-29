import socket
import ssl
def interact(cert,host ,port ,data="id"):

    #Needs cert and key generated:
    #openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365


    context = ssl.SSLContext() #Defaults to TLS 
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cert)
    with socket.create_connection((host, port)) as sock:
        #Create secure socket
        ssock=context.wrap_socket(sock, server_hostname=host)
        print(ssock.version())
        print(ssock.getpeercert())
        ssock.send(data.encode())
        while 1:
            recieve = ssock.recv(1024)
            if (recieve  !=0):
                break
            print(f"Recieved: {recieve}")
        print(f"Recieved: {recieve}")
        ssock.shutdown(2) #Nicely close the encrypted channel
if __name__=="__main__":
    port = 4000
    host= '192.168.237.129'
    cert="./cert.pem"
    key="./key.pem"
    argument=("relay 192.168.237.133 3000 ls")
    interact(cert ,host ,port ,argument)