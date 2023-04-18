from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

from .models import *
import os
import face_recognition as fr
import time
import pickle
import socket


def home(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            actual_user = LoginData.objects.get(username=username)
            actual_pass = actual_user.password

            if(actual_user == actual_user and actual_pass == password):
                return HttpResponseRedirect('/upload')
        except LoginData.DoesNotExist:
            print("Error User Not found...   🥲")

    return render(request, 'home.html', {})


def upload(request):
    if request.method == 'POST' and request.FILES.getlist('images'):
        name = request.POST.get('name', '')
        rollnum = request.POST.get('rollnum', '')
        mail = request.POST.get('mail', '')
        phone = request.POST.get('phone', '')
        dept = request.POST.get('dept', '')

        # Handle image upload
        images = request.FILES.getlist('images')
        print(images)
        fs = FileSystemStorage(location=f'{os.path.abspath("")}\images\\')
        filenames = []
        for image in images:
            filename = fs.save(f'{rollnum}_{image.name}.jpg', image)
            filenames.append(filename)
        print(f'{os.path.abspath("")}\images\{rollnum}')

        image_data = HashData(name=name, rollnum=rollnum, mail=mail, phnum=phone,
                              dept=dept, img=f'{os.path.abspath("")}\images\{rollnum}')
        image_data.save()
        print(os.path.abspath(""))
    return render(request, 'upload.html', {})

def trainModel(request):
    db_path = f'{os.path.abspath("")}\images\\'
    files = os.listdir(db_path)
    imgs = []
    cls_names = []
    n = 1

    for file in files:
        if(file[-4:] == ".JPG" or file[-4:] == ".jpg"):
            full_path = db_path + file
            im = fr.load_image_file(full_path)
            # im = cv2.resize(im, (500,500))
            print(im.shape)
            imgs.append(im)
            cls_names.append(file.split()[0])

            print("%1d of %2d is done" % (n, len(files)))
            n += 1

    known_face_encodings = []
    known_face_locations = []
    n = 1

    for img in imgs:
        start_time = time.time()
        # try:
        location = fr.face_locations(img)
        known_face_locations.append(location[0])
        print("location", location[0])
        # land = fr.api.face_landmarks(img, model='small')

        # encode the first face in the image
        encoding = fr.api.face_encodings(img, known_face_locations=location)
        known_face_encodings.append(encoding[0])
        print(encoding[0])

        print(n, img.shape, time.time()-start_time)
        n += 1

    # create a pickle file
    file = open(os.path.abspath("")+'\models\encode.pickle', 'wb')
    # dump encoding in pickle file
    send_list = []
    send_list.append(known_face_encodings)
    send_list.append(cls_names)

    pickle.dump(send_list, file)
    file.close()

    # Open a socket and connect to the receiving machine
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.8.114', 12345)
    sock.connect(server_address)

    # Load the data that you want to send from a pickle file
    with open('models\encode.pickle', 'rb') as f:
        data = pickle.load(f)

    # Send the data over the socket
    sock.sendall(pickle.dumps(data))

    data = {'message': 'Data Sent!'}
    return JsonResponse(data)

