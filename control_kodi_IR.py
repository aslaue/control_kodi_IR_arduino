#!/usr/bin/env python
# coding: utf-8

# In[4]:


import serial # pip install pyserial
#import clipboard # pip install clipboard
import requests # pip install requests
import json
import subprocess
import threading
import time


# In[69]:


code_panasonic={
    # "power" : "b'D5AD0B51\r\n'",
    # "sleep" : "b'422122AE\r\n'",
    # "clock/timer" : "b'4C2435D6\r\n'",
    # "clock_play": "b'1CF1449E\r\n'",
    # "auto off": "b'B90B1A6E\r\n'",
    # "dimmer": "b'E9F094A0\r\n'",
    # "display": "b'9F07EB9F\r\n'",
    "program": "b'E7964C2C\r\n'",
    "clear": "b'DCD31984\r\n'",
    "play mode": "b'DCD31984\r\n'",
    "repeat": "b'521A15E1\r\n'",
    # "0": "b'4F09DFF1\r\n'",
    # "1": "b'E8289565\r\n'",
    # "2": "b'66800DCD\r\n'",
    # "3": "b'C03CA26F\r\n'",
    # "4": "b'490541DF\r\n'",
    # "5": "b'B1CE824B\r\n'",
    # "6": "b'6F6EBBF3\r\n'",
    # "7": "b'71C5BE49\r\n'",
    # "8": "b'FA8E5DB9\r\n'",
    # "9": "b'E07C3D41\r\n'",
    "DEL": "b'20AB528\r\n'",
    # "10": "b'B55375F4\r\n'",
    # "album_prev": "b'CB7A2B0C\r\n'",
    # "album_next": "b'83880260\r\n'",
    "next": "b'CD09CA43\r\n'",
    "prev": "b'CA08C419\r\n'",
    # "play_CD": "b'43097087\r\n'",
    # "play_USB": "b'96C06D46\r\n'",
    # "play_option": "b'AF5D4ED6\r\n'",
    "stop": "b'5CD12DA9\r\n'",
    # "tuner/band": "b'61EC5A44\r\n'",
    "up": "b'E31BD4AC\r\n'",
    "down": "b'A8B3BFB2\r\n'",
    # "vol+": "b'DE5526F7\r\n'",
    # "vol-": "b'8C549057\r\n'",
    "enter": "b'CBA5A6D0\r\n'",
    "music port": "b'75D994CE\r\n'",
    # "bass treble": "b'721C8DE4\r\n'",
    # "preset eq": "b'54308B58\r\n'",
    # "surround": "b'8338D299\r\n'",
    # "muting": "b'542E29C9\r\n'"
}


# In[29]:


commande_panasonic={
    "program": "", # close 30 min
    "clear": "Playlist.Clear",
    "play mode_on": ("Player.SetShuffle",{"playerid":0,"shuffle":True}), #  {"jsonrpc":"2.0","method":"Player.SetShuffle","params":{"playerid":0,"shuffle":true},"id":1} -- shuffle on
    "play mode_off": ("Player.SetShuffle",{"playerid":0,"shuffle":False}), #  {"jsonrpc":"2.0","method":"Player.SetShuffle","params":{"playerid":0,"shuffle":true},"id":1} -- shuffle on
    "repeat_all": ("Player.SetRepeat", { "playerid": 0, "repeat": "all" }), #  {"jsonrpc": "2.0", "method": "Player.SetRepeat", "params": { "playerid": 0, "repeat": "one" }, "id": 1} -- repeat one /all / none
    "repeat_none": ("Player.SetRepeat", { "playerid": 0, "repeat": "none" }),
    "DEL": "System.Shutdown",
    "next": ("Player.GoTo",{"to": "next", "playerid":0}), #  {"jsonrpc": "2.0", "method": "Player.GoTo", "params": { "playerid": 0, "to": "next" }, "id": 1} -- next
    "prev": ("Player.GoTo",{"to": "previous", "playerid":0}), #  {"jsonrpc": "2.0", "method": "Player.GoTo", "params": { "playerid": 0, "to": "previous" }, "id": 1} -- next
    "stop": ("Player.Stop", {"playerid": 0}), #  {"jsonrpc": "2.0", "method": "Player.Stop", "params": { "playerid": 0 }, "id": 1} -- stop
    "up": ("Application.SetVolume",{"volume": "increment"}), #  { "jsonrpc": "2.0", "method": "Application.SetVolume", "params": { "volume": "increment" }, "id": 1 } -- volume up
    "down": ("Application.SetVolume",{"volume": "decrement"}), #  { "jsonrpc": "2.0", "method": "Application.SetVolume", "params": { "volume": "decrement" }, "id": 1 } -- volume up
    "enter": ("Player.PlayPause", {"playerid": 0}),#  ("Player.PlayPause", {"playerid": 0}) # {"jsonrpc": "2.0", "method": "Player.PlayPause", "params": { "playerid": 0 }, "id": 1} -- play pause
    "music port": "", # kodi-standalone
}
#https://www.programcreek.com/python/example/79076/xbmc.executeJSONRPC
#https://kodi.wiki/view/JSON-RPC_API/Examples
#https://forum.kodi.tv/showthread.php?tid=183394


# ### Fonction qui permet d'envoyer la commande sur Kodi

# In[56]:


# Configuration
kodi_ip = "192.168.0.33"
kodi_port = "8080"  # Par défaut : 8080
kodi_user = "kodi"
kodi_password = "qwertz"

# Endpoint pour l'API JSON-RPC de Kodi
kodi_endpoint = f"http://{kodi_ip}:{kodi_port}/jsonrpc"

# Fonction pour envoyer une commande à Kodi
def send_kodi_command(method, params=None):
    headers = {'Content-Type': 'application/json'}
    auth = (kodi_user,kodi_password)
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    response = requests.post(kodi_endpoint, headers=headers, auth=auth, data=json.dumps(data))    
#    response = requests.post(kodi_endpoint, headers=headers, data=json.dumps(data))
    return response.json()

# result = send_kodi_command("Player.PlayPause", {"playerid": 0})
# str1="next"
# result = send_kodi_command(*commande_panasonic[str1])
# print(result)


# ### Permet d'obtenir l'information du shuffle/repeat

# In[38]:


def get_kodi_property(property_type):
    # URL JSON-RPC de Kodi
    kodi_url = f"http://{kodi_ip}:{kodi_port}/jsonrpc"

    # Paramètres de la requête JSON-RPC pour obtenir l'état de la propriété
    request_json = {
        "jsonrpc": "2.0",
        "method": "Player.GetProperties",
        "params": {
            "playerid": 0,
            "properties": [property_type],
        },
        "id": 1,
    }

    # Envoi de la requête POST JSON
    response = requests.post(kodi_url, json=request_json)

    # Vérification de la réponse
    if response.status_code == 200:
        data = response.json()
        if "result" in data and property_type in data["result"]:
            property_state = data["result"][property_type]
            return property_state
        else:
            print(f"Impossible de récupérer l'état de la propriété {property_type}.")
            return None
    else:
        print(f"Erreur lors de la requête : Code {response.status_code}")
        return None

# Exemple d'utilisation pour obtenir l'état du mode shuffle
# shuffle_state = get_kodi_property("repeat")
# # shuffle_state = get_kodi_property("shuffled")

# if shuffle_state is not None:
#     print(f"Le mode shuffle est activé : {shuffle_state}")


# ### fonction qui envoie "pause" après un timer

# In[53]:


def timer_thread(duration_minutes, callback_function):
    time.sleep(duration_minutes * 60)
    callback_function()

def set_timer_and_pause_kodi(duration_minutes):
    # Lancer un thread pour le minuteur
    timer_thread_instance = threading.Thread(target=timer_thread, args=(duration_minutes, lambda: pause_kodi()))

    # Démarrer le thread
    timer_thread_instance.start()

def pause_kodi():
    # Envoyer une commande pour mettre en pause la lecture sur Kodi
    result = send_kodi_command("Player.PlayPause",{"playerid":0,"play":False})

    # Vérification de la réponse
    # if result.status_code == 200:
    #     print("La lecture sur Kodi a été mise en pause après le minuteur.")
    # else:
    #     print(f"Erreur lors de la requête : Code {response.status_code}")


# timer_duration_minutes = 0.1
# set_timer_and_pause_kodi(timer_duration_minutes)

# Le script peut continuer à exécuter d'autres tâches pendant que le minuteur fonctionne en arrière-plan.
# ...


# # écoute et retrouve si correspondance

# In[119]:

port="/dev/ttyACM0"
try:
    arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
except:
    raise Exception("La connexion avec l'Arduino n'a pas pu se faire\n\
    Vérifier que le port soit bien {}. Il est aussi possible que l'ordinateur n'y ait pas accès.\n\
    Dans ce cas là, executer \"sudo chmod a+rw {}\" dans un terminal puis redémarrez le script".format(port,port))

#from ... import Code_Panasonic
#dict = Code_Panasonic.code_panasonic
dict = code_panasonic

print("listening...")
Continue=True
while Continue==True:
	data=arduino.readline()
	if "b''" not in str(data):
		# nb_pulse_recu+=1
		# data_format = str(data[2:-5])
		data_format = str(data)[2:-5]
		# print("data",str(data)[2:-5])
		# print("data_format",data_format,"type",type(data_format))
		# if str(data) not in record_data:
		#     record_data.append(str(data))

		for i in range(len(dict)):
			key = list(dict.keys())[i]
			value = str(dict[key])[2:-3]
			# print("value",value,"type",type(value))
			if data_format == value:
				print("key",key)
				#Continue=False
				# break
				send_kodi_command_var = True
				if key == "program":  # close 30 min
					#qqch a coder ici
					timer_duration_minutes = 30
					set_timer_and_pause_kodi(timer_duration_minutes)
					send_kodi_command_var=False
				elif key == "music port":# kodi-standalone
					#qqch à coder ici
					send_kodi_command_var
					commande_ps = "ps -e | grep kodi-standalone"
					result_ps =  subprocess.run(commande_ps,shell=True, capture_output=True, text=True)
					if result_ps =="":
						subprocess.run("kodi-standalone",shell=True, capture_output=True, text=True)
				elif key =="play mode": 
					if get_kodi_property("shuffled")==True:
						key = "play mode_off"
					else:
						key = "play mode_on"
				elif key == "repeat":
					if get_kodi_property("repeat") == "off":
						key == "repeat_all"
					else:
						key == "repeat_none"

				if send_kodi_command_var == True:
					result = send_kodi_command(*commande_panasonic[key])


# ## ancienne commande panasonic

# In[21]:


# commande_panasonic={
#     "power" : "",
#     "sleep" : "",
#     "clock/timer" : "",
#     "clock_play": "",
#     "auto off": "",
#     "dimmer": "",
#     "display": "",
#     "program": "", # close 30 min
#     "clear": "Playlist.Clear",
#     "play mode": "", #  {"jsonrpc":"2.0","method":"Player.SetShuffle","params":{"playerid":0,"shuffle":true},"id":1} -- shuffle on
#     "repeat": "", #  {"jsonrpc": "2.0", "method": "Player.SetRepeat", "params": { "playerid": 0, "repeat": "one" }, "id": 1} -- repeat one /all / none
#     "0": "",
#     "1": "",
#     "2": "",
#     "3": "",
#     "4": "",
#     "5": "",
#     "6": "",
#     "7": "",
#     "8": "",
#     "9": "",
#     "DEL": "System.Shutdown",
#     "10": "",
#     "album_prev": "", #
#     "album_next": "", #
#     "next": ("Player.GoTo",{"to": "next", "playerid":0}), #  {"jsonrpc": "2.0", "method": "Player.GoTo", "params": { "playerid": 0, "to": "next" }, "id": 1} -- next
#     "prev": ("Player.GoTo",{"to": "previous", "playerid":0}), #  {"jsonrpc": "2.0", "method": "Player.GoTo", "params": { "playerid": 0, "to": "previous" }, "id": 1} -- next
#     "play_CD": "",
#     "play_USB": "",
#     "play_option": "",
#     "stop": "", #  {"jsonrpc": "2.0", "method": "Player.Stop", "params": { "playerid": 0 }, "id": 1} -- stop
#     "tuner/band": "",
#     "up": ("Application.SetVolume",{"volume": "increment"}), #  { "jsonrpc": "2.0", "method": "Application.SetVolume", "params": { "volume": "increment" }, "id": 1 } -- volume up
#     "down": ("Application.SetVolume",{"volume": "decrement"}), #  { "jsonrpc": "2.0", "method": "Application.SetVolume", "params": { "volume": "decrement" }, "id": 1 } -- volume up
#     "vol+": "",
#     "vol-": "",
#     "enter": ("Player.PlayPause", {"playerid": 0}),#  ("Player.PlayPause", {"playerid": 0}) # {"jsonrpc": "2.0", "method": "Player.PlayPause", "params": { "playerid": 0 }, "id": 1} -- play pause
#     "music port": "", # kodi-standalone
#     "bass treble": "",
#     "preset eq": "",
#     "surround": "",
#     "muting": ""
# }
# #https://www.programcreek.com/python/example/79076/xbmc.executeJSONRPC
# #https://kodi.wiki/view/JSON-RPC_API/Examples
# #https://forum.kodi.tv/showthread.php?tid=183394
