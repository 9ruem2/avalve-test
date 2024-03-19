from importlib.metadata import files 
import requests
import socketio
import json

import time
import os

sio = socketio.Client()

# sio = socketio.Client(logger=True, engineio_logger=True,ssl_verify=True)


@sio.event
def connect():
    print("Connected to server")
    
@sio.event
def disconnect():
    print('Disconnected from server')

@sio.event
def connect_error(err):
    print(err)
    # time.sleep(2)

# @sio.event
# def receive_uuid(data):
#     print('uuid', data)
#     writeuuidInfo(file_path,data)  
    


@sio.event
def upload_start(msg):
    
    head_response = requests.head('http://localhost:3000/uploads/status', headers={"device_owner" : "Avalve", "device_name": "eunhee","status" : "upload_start","token" : msg})
    
    print(head_response)


    # secondHeaders = {"device_owner" : "Avalve", "device_name": "eunhee", "token" : msg}

    # json_list = os.listdir(os.path.join(os.getcwd()+jsonDir))
    # json_files = getFilesList(json_list,json_type,jsonDir)
    # json_response = requests.post(url2,files=json_files,headers=secondHeaders)
    
    # image_list = os.listdir(os.path.join(os.getcwd()+imageDir))
    # for value in image_list:   
    #     image_response = requests.post(url1,files=[('imageFile', (value, os.path.join(os.getcwd()+imageDir+'/'+str(value)),'rb'))],headers=secondHeaders)
    #     print(image_response.text)
    
    # # upload_finish HEAD REQEUST
    # head_response = requests.head('http://localhost:3000/upload/status', headers={"device_owner" : "Avalve", "device_name": "eunhee", "status" : "upload_finish","token" : msg})
    
    print(msg)

def configs():
    global file_path, num
    global config
    global Manufacturer,Device_model,Device_name,Device_owner,Device_uuid
    global url1, url2, url3
    global imageDir, jsonDir, img_type, json_type 
    

    file_path = "./info.json"
    num ="one"
    
    with open(file_path, 'r') as f:
        config = json.load(f)
    
    Manufacturer = config[num]['SmartFarm']['Manufacturer']
    Device_model = config[num]['SmartFarm']['Device_model']
    Device_owner = config[num]['SmartFarm']['Device_owner']
    Device_name = config[num]['SmartFarm']['Device_name']
    Device_uuid = config[num]['Auth']['Device_uuid']
   
    
    url1 = 'http://localhost:3000/upload/image'
    url2 = 'http://localhost:3000/upload/json'
    # url3 = 'https://avalve-smartfarm.tk:8888/reset'

    imageDir = '/image'
    jsonDir = '/json'
    img_type = 'image/jpg'
    json_type = 'application/json'


def getFilesList(some_list,some_type,dir):
    new_list = []
    for row in enumerate(some_list):
        new_list.append((
            'jsonFile',
            (row,open(os.path.join(os.getcwd()+dir+'/'+str(row)),'rb'),some_type)
        ))
    return new_list

def send_msg_start():
    while True:
        print(sio.connected)
        
        sio.emit("make_token", "upload start!")
        time.sleep(120)






#  메인함수 실행
if __name__ == '__main__':
    
    configs()
    sio.connect('http://localhost:3000',
                headers = {
                "manufacturer": "AvalveFarm",
                "device_model": "0x11",
                "device_owner": "Avalve",
                "device_name": "eunhee"
                },
                auth =
                {
                "device_uuid": "df03a831-8d1b-4d6d-a039-bd8bdc32975a"
                }
                )
    send_msg_start()
    sio.wait()
