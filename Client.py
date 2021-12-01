import socket
import ssl
import PySimpleGUI as sg
from subprocess import run
import os

def interact(cert ,key ,host ,port, data="0"):
    """
        Description:

            Allow commands to be recieved from a specific port and IP address to be then executed
            on this machine (controller) and sent back (including the choice of relay). Bidirectional 
            encryption is also used with SSL (Secure Socket Layer). 

        Arguments:

            cert  -- Location of the cerificate for authentication
            key   -- Location of the key for authentication
            host  -- The ip address of the server
            port  -- The port to bind with
            data  -- Which command will be executed
    """

    context = ssl.SSLContext()                                             #Managers the SSL settings
    context.load_cert_chain(certfile=cert, keyfile=key)                    #Loads the certification file and Key to allow back to back encyption

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:     #creates a socket that listens and binds to an IP and Port
        sock.bind((host, port))
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as ssock:
            while 1:
                conn, addr = ssock.accept()                                #Waits for the client to accept a connection and print connected
                print('Connected by', addr)
                while 1:                                                   #Creates a continuel loop that looks for data to be recieved 
                    recieve = conn.recv(1024)                              
                    if (recieve  !=0):
                        break                                              #Breaks out the loop once data is recieved and gives an output
                    print(f"Recieved: {recieve}")
                recieve=recieve.decode()                                   #Convert the data to a list to allow for the relay command to be checked
                command_split=recieve.split(" ")
                if (command_split[0]=="relay"): 
                    host=command_split[1]                                  #Breaks the list down into port and IP variables for easier communication
                    port=command_split[2]
                    command=command_split[3]
                    os.system("python3 relay.py -u "+str(host)+" -p "+str(port)+" -c "+str(command)) #Send paramters of a new port and IP to the test.py file to allow relay to occur
                else:
                    try:                                                                      
                    	command = run(command_split, capture_output=True).stdout              #runs the recieved command and sends the result of the command back
                    	conn.send(command)                                                    
                    except:
                        error=("error with the command")                 #returns and error if command failed
                        conn.send(error.encode())
                        print("error with the command")
def get_host_info():
    """
        Description:

            Gets the host IP address and returns the value

        Arguments:
            None

        Returns:
            the host/IP of the current system
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                                      #Uses a socket and standard port (80) and address(8.8.8.8) to retrieve the IP
    s.connect(("8.8.8.8", 80))
    host=(s.getsockname()[0])
    s.close()                                                                                 #Closes the connection
    return host                                                                               #Returns the address
if __name__=="__main__":
    port = 4000                                                                               #Hardcodes the values; port, cert, key as default
    cert="./cert.pem"
    key="./key.pem"
    host=get_host_info()                                                                      #Retrives the IP from the function get_host_info 
    interact(cert, key, host ,port)                                                           #Calls the function interact with the;cert ,key ,host and port 
