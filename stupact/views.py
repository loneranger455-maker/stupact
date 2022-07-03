from email.policy import default
from pathlib import Path
from django.http import HttpResponse
from django.shortcuts import redirect, render
from requests import delete, session
from dataforstupact.models import mymodel
import os
def signup(request):
        error=""
        username=""
        email=""
        fname=""
        lname=""
        try:
            username=request.POST.get("username") 
            fname=request.POST.get("fname")
            lname=request.POST.get("lname")
            email=request.POST.get("email")
            password=request.POST.get("password")
            password_confirm=request.POST.get("confirm")
            faculty=request.POST.get("faculty")
            batch=request.POST.get("batch")
            allobjects=mymodel.objects.all()
            allobjects1=[i.username for i in allobjects]
            allobjects2=[i.email for i in allobjects ]
       
            if len(fname)<3 or len(lname)<3:
                error="First and last name must be at least 3 characters long"
            elif email[-10:]!="@gmail.com":
                error="Email format is incorrect"
            elif email in allobjects2:
                error="User already registered from this email"
            elif len(username)<5:
                error="Username must be at least 5 characters long"
            elif username in allobjects1:
                error="Username already exist"
            elif len(password)<8:
                error="Password must be at least 8 characters long"
            elif password!=password_confirm:
                error="password fields don't match"
                
            elif faculty=="none" or batch=="none":
                error="Complete the select field"
            else:
                valuestobesaved=mymodel(first_name=fname,last_name=lname,email=email,password=password,username=username,batch=batch,faculty=faculty)
                valuestobesaved.save()
                return redirect('/')
               
        except:
            pass
        


  
        print(error)
        data={
            "error":error,
            "username":username,
            "email":email,
            "firstname":fname,
            "lastname":lname,
        }
        for i in data:
            if data[i]==None:
                data[i]=""
           

        
       

        return render(request,"signup.html",data)
def services(request):
    return render(request,"services.html")

def home(request):
    validate=request.session.get("Username",default=None)
    if validate==None:
        return redirect("/login")
    
    return render(request,"home.html")
def login(request):
    usernm=request.POST.get("username")
    password=request.POST.get("password")
    error=" "
    sym1=sym2=" "
    if usernm!=None and password!=None:
        try:
            allobjects=mymodel.objects.get(username=usernm)
            print(password)
            if(allobjects.password!=password):
                error="wrong password"
                sym1="✔"
                sym2="✘"
            else:
                request.session["Username"]=allobjects.username
                request.session["first_name"]=allobjects.first_name
                request.session["last_name"]=allobjects.last_name
                request.session["email"]=allobjects.email
                request.session["faculty"]=allobjects.faculty
                request.session["batch"]=allobjects.batch
                request.session["image"]=allobjects.image.url
               
                return redirect('/home')

        
                    
        except:
            error="user dont exist"
            sym1="✘"
    else:
        usernm=" "
    
    data={"error":error,
            "username":usernm,
            "sym1":sym1,
            "sym2":sym2
    }
    return render(request,"index.html",data)
def start(request):
    if request.session.get("Username",default=None)==None:
        return redirect('/login')
    else:
        return redirect('/home')
 
        
def user(request):
    allobjects=mymodel.objects.get(username=request.session["Username"])
    if request.method == "POST":
        image1=request.FILES["img"]
        temp=allobjects.image.url
        try:
             os.remove(str(Path(__file__).resolve().parent.parent)+temp)
        except:
            pass
        print(temp)
        allobjects.image=image1
        allobjects.save()
        request.session["image"]=allobjects.image.url
    
    data={"username":request.session["Username"],
    "name":request.session["first_name"]+" "+request.session["last_name"],
    "email":request.session["email"],
    "faculty":request.session["faculty"]+" ("+request.session["batch"]+")",
    "image":allobjects.image,
    }
    return render(request,"username.html",data)

def logout(request):
    request.session.flush()
    return redirect('/login')