from django.shortcuts import render
from .models import Attend

# Create your views here.
def attend_view(request):
  status = None
  if request.method == "POST":
    if request.user.is_authenticated:
      try:
        attended_datetime = str(Attend.objects.get(attender=request.user).datetime)[:10]
      except:
        pass

      try:
        attended_today = Attend.objects.filter(attender=request.user,datetime__startswith=attended_datetime)
        status =2
      except:
        status =3


      if status == 3:

        attend_object = Attend(attender=request.user)
        attend_object.save()
        status = 1

    else:
      status = 0

  return render(request, 'attend.html',{'status':status})