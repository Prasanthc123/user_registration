from django.shortcuts import render
from django.http import HttpResponse
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
            return HttpResponse('data submitted')
        else:
            return HttpResponse('in valid')
    return render(request,'registration.html',context=d)