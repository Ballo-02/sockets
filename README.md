# C&C (Controller and Client) Script Project
A project intended for my 2nd year Ethical Hacking and Cyber Security degree which involves a client (can be multiple scripts each on different machines) and a controller that will control these client scripts. You can send live commands to each client, relay a command (send a command from one client to the next), send python commands and send general useful commands used for enumerating a machine. This can all be selected from the GUI (Graphical User Interface) menu when the script is run. The client will be constantly running in the background which will generate a key that needs to be shared across to the controller so that all information is encrypted when communicating from one machine to the next. Therefore, eliminating any possible sensitive data to be stolen. If any command sent cause an error the script has a built-in error handling service with a GUI strip telling the user if the controller is connected to the client or disconnected.

## Author

|   Name              |    Username     |
|---------------------|-----------------|
| Owen Ball           |   Ballo-02      |

## What's in this repository?

### `Client.py`
This is the script which can be placed on multiple machines that once run is in a constant loop until commands aren’t sent to it. It will require the certificate to be created as well as the key

### `Controller.py`
Using this script, you can control multiple client.py scripts as long as they're running and have the correct certificate and key. You can send live commands to each client, relay a command (send a command from one client to the next), send python commands and send general useful commands used for enumerating a machine

### `Relay.py`
Allows the script to relay information to another client so forth with the correct information

### `cert.pem`
Certificate to allow encrypted transmission to occur via the Controller and Client

### `key.pem`
Key to allow encrypted transmission to occur via the Controller and Client
