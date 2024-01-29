# IR Kodi Controller
Allows to control your Raspberry pi running Kodi with an IR Remote, an Arduino board and an IR sensor
## In short
1) Flash the .ino file to an Arduino board
2) (if needed) create a virtual environment "venv_kodi"
3) download the pip library pyserial, request (and clipboard for attribute_remote_key_code.py)
4) plug the arduino board and execute the bash script
## Material
This script asssumes that you have a Raspberry pi (it has been tested with the RPI3) with Raspberry pi os that has kodi-standalone installed, an Arduino board, and an infrared sensor (mine was VS1838). The Arduino Board is configured with the provided .ino file that displays the IR code received on the Serial. The kodi python script will read the Serial and choose what command to send to kodi.  
Since it sends the commend with the http POST/GET protocol, it can be executed from an eventual other device.

The other script (attribute_tremote_key_code.py) aims to determine the hexadecimal code from the remote. In my case, my remote does wierd things, such as sending "noise" in addition to the corresponding code. It records the code and print the one that is repeated the most.   

The bash script is needed since the RPI needs the python library, and uses a virtual environnement, so it calls the venv before 

## Funtionning
The script control_kodi_IR.py contains the correspondance between the hexadecimal codes of the <insert remote name here> and the the function. It can be also set in an external file

## Assignation
I assigned the following button and effects:
- 
