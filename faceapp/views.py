from django.shortcuts import render,redirect
from .models import Attend
from django.utils import timezone
from django.contrib import messages
from .forms import NewPhotoForm
from django.http import HttpResponse

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