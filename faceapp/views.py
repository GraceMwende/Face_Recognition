from django.shortcuts import render,redirect
from .models import Attend
from django.utils import timezone
from django.contrib import messages
from .forms import NewPhotoForm
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# face recognition
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

def home(request):
  return render(request,'home.html')

def dashboard(request):
  if(request.user.username == 'admin'):
    print('admin')
    return render (request, 'admin.html')

  else:
    print('not admin')
    messages.error(request,'You are not an admin')
    return render(request, 'staff.html')

def upload_photos(request):
  if request.method == 'POST':
      form = NewPhotoForm(request.POST, request.FILES)
      if form.is_valid():
          form.save()
      messages.success(request, 'Image successfully uploaded')
      return redirect('dashboard')

  else:
      form = NewPhotoForm()
  return render(request, 'new_photo.html', {"form": form})

def create_user(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      messages.success(request, f'Staff registered successfully!')
      return redirect('dashboard')

  else:
    form = UserCreationForm()

  return render(request, 'admin-register.html',{'form':form})
  
def face_attend_view(request):
  path = 'media/training_images'
  images = []
  personNames = []
  myList = os.listdir(path)
  print(myList)
  for cu_img in myList:
      current_Img = cv2.imread(f'{path}/{cu_img}')
      images.append(current_Img)
      personNames.append(os.path.splitext(cu_img)[0])
  print(personNames)

  # function to encode all the train images 
  def faceEncodings(images):
      encodeList = []
      for img in images:
          img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
          encode = face_recognition.face_encodings(img)[0]
          encodeList.append(encode)
      return encodeList


  def attendance(name):
      with open('Attendance.csv', 'r+') as f:
          myDataList = f.readlines()
          nameList = []
          for line in myDataList:
              entry = line.split(',')
              nameList.append(entry[0])
          if name not in nameList:
              time_now = datetime.now()
              tStr = time_now.strftime('%H:%M:%S')
              dStr = time_now.strftime('%d/%m/%Y')
              f.writelines(f'\n{name},{tStr},{dStr}')


  encodeListKnown = faceEncodings(images)
  print('All Encodings Complete!!!')

  # take pictures from webcam 
  cap = cv2.VideoCapture(0)

  while True:
      ret, frame = cap.read()
      if ret:
          faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)

      else:
          break
          faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

      facesCurrentFrame = face_recognition.face_locations(faces)
      encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

      for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
          matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
          faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
          # print(faceDis)
          matchIndex = np.argmin(faceDis)

          if matches[matchIndex]:
              name = personNames[matchIndex].upper()
              # print(name)
              y1, x2, y2, x1 = faceLoc
              y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
              cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
              cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
              cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
              attendance(name)

      cv2.imshow('Webcam', frame)
      if cv2.waitKey(1) == 13:
          break

  cap.release()
  cv2.destroyAllWindows()
  return redirect('home')


# Create your views here.
def attend_view(request):
  status = None
  if request.method == "POST":
    if request.user.is_authenticated:
      try:
        attended_datetime = str(timezone.now())[:10]
        print(attended_datetime)
      except:
        pass


      attended_today = Attend.objects.filter(attender=request.user,datetime__startswith=attended_datetime)
      
      if str(attended_today)[10:] == "[]>":
        status =3

      else:
        status=2

      if status == 3:

        attend_object = Attend(attender=request.user)
        attend_object.save()
        status = 1

    else:
      status = 0

  return render(request, 'attend.html',{'status':status})