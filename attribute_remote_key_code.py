# # affectation des boutons et code hexa
import serial

port="/dev/ttyACM0"
#sudo chmod a+rw /dev/ttyACM0
arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
record_data=[]
record_data_count=[]
nb_pulse_recu=0
nb_appui_touche=10
print("appuyer {}x sur le bouton souhaité".format(nb_appui_touche))
while nb_pulse_recu<20:
    data=arduino.readline()
    if "b''" not in str(data):
        nb_pulse_recu+=1
        print(str(data))
        # if str(data) not in record_data:
        #     record_data.append(str(data))
        found=0
        for k,j in enumerate(record_data):
            if str(data)==j:
                found=1
                record_data_count[k]+=1
                break
        if found==0:
            record_data.append(str(data))
            record_data_count.append(1)


# # In[68]:


for k,j in enumerate(record_data):
    if record_data_count[k]>1:
        print(j,record_data_count[k]/nb_appui_touche)
print("")
for k,i in enumerate(record_data_count):
    if i == max(record_data_count):
        most_frequent_code=record_data[k]
        break
if most_frequent_code in list(code_panasonic.values()):
    print("ATTENTION, repetition probable")
else:
    print(most_frequent_code)
    clipboard.copy(most_frequent_code)


