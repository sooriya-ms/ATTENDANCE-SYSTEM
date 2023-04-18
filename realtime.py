import face_recognition as fr
import cv2
import time
import numpy as np
import socket
import pickle
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import collections
from datetime import datetime

# initialize Firebase
cred = credentials.Certificate('attendance-system-54923-firebase-adminsdk-889ld-23bd754a59.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://attendance-system-54923-default-rtdb.firebaseio.com/'
})  

def addToCloud(rollnum):
    # Retrieve the register number node from the database
    idd = 1
    reg_num_node = db.reference(f'attendance detail/{rollnum}')
    reg_num_id = db.reference(f"attendance detail/{rollnum}/idd")
    data = reg_num_node.get()

    print("data", data)
    if(data == None):
        cur_time = time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())
        reg_num_node.set({
            "1":{
                "in_time": cur_time,
                "out_time": ""
            }
        })
    else:
        # Sort the numbers by their keys and retrieve the last one
        largest_num = reg_num_node.order_by_key().limit_to_last(1).get()

        last_data_key = '-1'
        last_data_val = {}
        if(not isinstance(largest_num, collections.OrderedDict)):
            if(largest_num[0] == None):
                last_data_key = '1'
                last_data_val = largest_num[1]
        else:
            last_data_key = list(largest_num.keys())[0]
            last_data_val = list(largest_num.values())[0]
        

        if(last_data_val['out_time'] == "" or last_data_val['out_time'] == None):
            
            date_time_obj = datetime.strptime(last_data_val["in_time"], "%m/%d/%Y, %H:%M:%S")
            epoch_seconds = int(date_time_obj.timestamp())
            if(epoch_seconds+300<time.time()):
                cur_time = time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())
                last_data_val['out_time'] = cur_time
                
                reg_num_node.update({
                last_data_key:last_data_val
                })
            else:
                print("come after some time")
        else:
            cur_time = time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())
            reg_num_node.update({
            str(int(last_data_key)+1):{
                "in_time": cur_time,
                "out_time": ""
            }
        })

def recognize_faces():
    global face_encodings
    face_encodings = []
    
    bef = []
    count = 0
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()

        face_locations = fr.face_locations(frame, model="hog")
        face_encodings = fr.face_encodings(frame, face_locations)
        print(face_locations)
        try:
            _1,_2,_3,_4 = face_locations[0]
        except:
            print("Face Not Detected🥲")
            continue

        cv2.rectangle(frame, (_4, _1), (_2, _3), (255, 0, 255), 2)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        for face_encoding in face_encodings:
            matches = fr.compare_faces(known_face_encodings, face_encoding, 0.5)
            face_dis = fr.face_distance(known_face_encodings, face_encoding)
            # print(face_dis)
            matchIndex = np.argmin(face_dis)
            # print(matchIndex)

            if True in matches and cls_names[matchIndex]:
                bef.append(matchIndex)
                count+=1
            if(count >= 1):
                count = 0
                result = all(element == bef[0] for element in bef)
                if(result):
                    name = cls_names[matchIndex].upper()
                    print(f"Welcome {name}!")
                    rollnum = name.split("_")[0]

                    addToCloud(rollnum=rollnum)
                else:
                    pass
            else:
                print("Access Denied")
    video_capture.release()
    cv2.destroyAllWindows()


# Open a socket and listen for incoming connections
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', 12345)  # Listen on all available interfaces
sock.bind(server_address)
sock.listen(1)

# Accept incoming connections and receive the pickled data
while True:
    connection, client_address = sock.accept()
    data = b''
    while True:
        chunk = connection.recv(1024)
        if not chunk:
            break
        data += chunk

    # Unpickle the data to access the original data
    data = pickle.loads(data)
    known_face_encodings = data[0]
    cls_names = data[1]
    print("known_face_encodings", known_face_encodings)
    print("cls_names", cls_names)
    
    # Run the face recognition in a separate thread
    thread = threading.Thread(target=recognize_faces)
    thread.start()