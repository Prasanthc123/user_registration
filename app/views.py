from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.forms import *
def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}

    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            mufdo=ufd.save(commit=False)
            pw=ufd.cleaned_data['password']
            mufdo.set_password(pw)
            mufdo.save()

            mpfdo=pfd.save(commit=False)
            mpfdo.username=mufdo
            mpfdo.save()

            send_mail('registration',
            'form register successfully',
            'cprasanth652@gmail.com',
            [mufdo.email],
            fail_silently=False,
            )
            return HttpResponse('data submitted')
        else:
            return HttpResponse('invalid data')
    return render(request,'registration.html',context=d)


def login_page(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Incorrect Username or Password.Please try again.')
    return render(request,'login_page.html')

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
@login_required
def display_profile(request):
    un=request.session.get('username')
    uo=User.objects.get(username=un)
    po=Profile.objects.get(username=uo)
    d={'uo':uo,'po':po}
    return render(request,'display_profile.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        print(UO)
        password=request.POST['password']
        print(password,UO.password)
        if UO.password==password:
            pw=request.POST['pw']
            print(pw)
            # username=request.session.get('username')
            # UO=User.objects.get(username=username)
            # UO.set_password(pw)
            # UO.save()
            return HttpResponse('change password sucessfully')
        else:
            return HttpResponse('old invalid')
    return render(request,'change_password.html')


def reset_password(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']

        LUO=User.objects.filter(username=username)
        if LUO:
            UO=LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('reset is done ')
        else:
            return HttpResponse('ur username is not in ur databasee')
    else:
        return render(request,'reset_password.html')