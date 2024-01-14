from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth import views,login,authenticate
from django.contrib import messages
from django.contrib.auth import mixins
from django.shortcuts import redirect,resolve_url,render
from .models import *
from django.db.models import Q
# Create your views here.
class Login(generic.TemplateView):
    template_name='accounts/login.html'
    
    def Login(request):
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=User.objects.filter(username=username)
        
        if not user.exists():
          messages.warning(request,"No User Found,Please Check Credentials") 
          return redirect('/accounts/login/')  
        user_obj=authenticate(username=username,password=password)
        if not user_obj:
            messages.warning(request,"Wrong Crdentials")
            return redirect('/accounts/login/')
        else:   
            login(request,user_obj)
            messages.success(request,"Login Succesful")
            if (user[0].is_superuser):
                return redirect('/clubs/')
            return redirect('/') 

def AddUser(request):
    if request.user.is_superuser:
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            type=request.POST.get('type')
            if not User.objects.filter(username=username).exists():
                obj=User.objects.create(
                        username=username
                    )
                obj.set_password(raw_password=password)
                obj.save()
                if type=="student":
                    Profile.objects.create(
                        user=User.objects.get(username=username),
                        is_student=True,
                    )
                else:
                    Profile.objects.create(
                        user=User.objects.get(username=username),
                        is_teacher=True,
                    )
                return redirect('/clubs/')
            else:
                messages.warning(request,"user already exists")
                return redirect('/accounts/adduser/')
        return render(request,'accounts/adduser.html')
    else:
        messages.warning(request,"You can't add user")
        return redirect('/clubs/')

class user(mixins.LoginRequiredMixin,generic.ListView):
    template_name="accounts/user.html"
    model=User
    context_object_name="users"

    def update(request,id):
        obj=Profile.objects.get(user__id=id)
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            type=request.POST.get('type')
            img=request.FILES.get('img')
        return render(request,'accounts/edit.html',{'prof':obj})