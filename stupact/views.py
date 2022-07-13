from email.policy import default
from pathlib import Path
from datetime import datetime
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
from requests import delete, session
from dataforstupact.models import mymodel
from dataforstupact.models import stumartmodel,order_list,notifications
import requests 
import os
import uuid
def signup(request):
        error=""
        username=""
        email=""
        sym1="✔"
        sym2="✘"
        symbol=["","","",""]
        # fname=""
        # lname=""
        try:
            username=request.POST.get("username") 
            # fname=request.POST.get("fname")
            # lname=request.POST.get("lname")
            email=request.POST.get("email")
            password=request.POST.get("password")
            password_confirm=request.POST.get("confirm")
            # faculty=request.POST.get("faculty")
            # batch=request.POST.get("batch")
            allobjects=mymodel.objects.all()
            allobjects1=[i.username for i in allobjects]
            allobjects2=[i.email for i in allobjects ]
       
            # if len(fname)<3 or len(lname)<3:
            #     error="First and last name must be at least 3 characters long"
            if username in allobjects1:
                error="Username already exist"
                symbol[0]=sym2
            elif email[-10:]!="@gmail.com":
                error="Email format is incorrect"
                symbol[0]=sym1
                symbol[1]=sym2
            elif email in allobjects2:
                error="User already registered from this email"
                symbol[0]=sym1
                symbol[1]=sym2
            elif len(username)<5:
                error="Username must be at least 5 characters long"
                symbol[0]=sym2
                symbol[1]=sym1
           
            elif len(password)<8:
                error="Password must be at least 8 characters long"
                symbol[0]=sym1
                symbol[1]=sym1
                symbol[2]=sym2
            elif password!=password_confirm:
                error="password fields don't match"
                symbol[0]=sym1
                symbol[1]=sym1
                symbol[2]=sym1
                symbol[3]=sym2                
            # elif faculty=="none" or batch=="none":
            #     error="Complete the select field"
            else:
                valuestobesaved=mymodel(email=email,password=password,username=username)
                valuestobesaved.save()
                valuestobesaved=notifications(username=username,notify="Welcome to stumart family.Hope you will like our services.",status="unseen")
                valuestobesaved.save()
                return redirect('/')
               
        except:
            pass
        data={
            "error":error,
            "username":username,
            "email":email,
           "symbol":symbol,
        }
        for i in data:
            if data[i]==None:
                data[i]=""
           

        
       
        print(error)
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
    return render(request,"login.html",data)
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
    return render(request,"account.html",{"object":allobjects,
    })

def logout(request):
    request.session.flush()
    return redirect('/login')


#stumart rendering function
def stumartfunc(request):
    variable=stumartmodel.objects.all()
    data=list()
    
    for i in variable:
        temp=dict()
        temp["id"]=i.id
        temp["username"]=i.username
        temp["title"]=i.title
        temp["image"]=i.image 
        temp["price"]=i.price  
        data.append(temp)
       
    data2={
        "itemlist":data,
    }
    return render(request,"stumart.html",data2)

#for product menu in stumart

def productmenu(request,tabvalue):
   if tabvalue=="myproducts":
            allobjects=stumartmodel.objects.all()
            allobjects=[i for i in allobjects if i.username==request.session["Username"] ]
            data=[]
            for i in allobjects:
                temp=dict()
                temp["username"]=i.username
                temp["title"]=i.title
                temp["image"]=i.image 
                temp["price"]=i.price  
                data.append(temp)
        
            data2={
            "itemlist":data,
        }
            return render(request, "stumart/myproducts.html",data2)
   elif tabvalue=="placeproduct":
        if request.method == "POST":
            title=request.POST.get("title")
            category=request.POST.get("category")
            price=request.POST.get("price")
            discription=request.POST.get("textbox")
            image=request.FILES["image"]
            varia=stumartmodel(username=request.session["Username"],category=category,price=price,title=title,details=discription,image=image)
            varia.save()
            return redirect('/stumart')
        return render(request, "stumart/placeproduct.html")
   elif tabvalue=="purchasehistory":
       
        allobjects=order_list.objects.all()
        buyerobjects=[i for i in allobjects if i.buyer==request.session["Username"] ]
        sellerobjects=[i for i in allobjects if i.seller==request.session["Username"] ]
        return render(request, "stumart/purchasehistory.html",{"buyer":buyerobjects,"seller":sellerobjects})
   else:
        return redirect('/stumart')


#for ordering product
def orderproduct(request,uniquevalue):
    allobjects=stumartmodel.objects.get(id=uniquevalue)
    if request.method=="POST":
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        phonenumber=request.POST.get("phone")
        region=request.POST.get("region")
        faculty=request.POST.get("faculty")
        batch=request.POST.get("batch")
        payment=request.POST.get("payment")
        if region=="hostel":
                disc=0
        elif region=="lamachaur":
                disc=20
        else:
                disc=50
        print(payment)
        if payment=="cod":
            save2=order_list(first_name=fname,last_name=lname,phonenumber=phonenumber,region=region,buyer=request.session["Username"],seller=allobjects.username,product=str(allobjects.id),delivery_charge=disc,price=allobjects.price,status="order verified",title=allobjects.title)
            save2.save()
            objforreward=mymodel.objects.get(username=request.session["Username"])
            objforreward.reward+=20
            valuestobesaved=notifications(username=request.session["Username"],notify="You have obtained 20 reward points for the order.Keep going..",status="unseen")
            valuestobesaved.save()
            valuestobesaved=notifications(username=request.session["Username"],notify="Thank you for the order.You have selected cash on delivery.You will get your product within some days.",status="unseen")
            valuestobesaved.save()
            return redirect('/stumart')
        elif payment=="esewa":
            url ="https://uat.esewa.com.np/epay/main"
           
            d = {'amt': allobjects.price,
                'pdc': disc,
                'psc': 0,
                'txAmt': 0,
                'tAmt': allobjects.price+disc,
                'pid':'ee2c3ca1-696b-4cc5-a6be-2c40d929d453',
                'scd':'EPAYTEST',
                'su':'http://merchant.com.np/page/esewa_payment_success?q=su',
                'fu':'http://merchant.com.np/page/esewa_payment_failed?q=fu'}
            resp = requests.post(url, d)
            print(resp)
    return render(request, "stumart/orderproduct.html",{"object":allobjects})

#for notifications
def sortit(objectvalue):
    for i in range(0,len(objectvalue)):
        for j in range(i+1,len(objectvalue)):
            if objectvalue[i].time<objectvalue[j].time:
                temp=objectvalue[i]
                objectvalue[i]=objectvalue[j]
                objectvalue[j]=temp

    return(objectvalue)

def notification(request):
    timecounter=[]
    allobjects=notifications.objects.all()
    allobjects=[i for i in allobjects if i.username==request.session["Username"] or i.username=="all"]
    allobjects=sortit(allobjects)
    notifylist=[]
    
    for i in allobjects:
            if i.status=="unseen":
                i.status="seen"
                i.save()
            
            notifylist.append(i.notify)
            diff=int(datetime.now().strftime("%Y%m%d%H%M%S"))-int(i.time)
            if(diff<100):
                    diff2=str(diff)+"sec"
            elif(diff<10000):
                    diff2=str(int(diff/100))+"min"
            elif(diff<1000000):
                    diff2=str(int(diff/10000))+"hr"
            elif(diff<100000000):
                    diff2=str(int(diff/1000000))+"day"
            else:
                    diff2=str(int(diff/1000000000))+"months"
            timecounter.append(diff2)
                   
    data={
        "notifications":notifylist,
        "counter":timecounter,
    }

       
    return JsonResponse(data)

def notificationcount(request):
    allobjects=notifications.objects.all()
    allobjects=[i for i in allobjects if i.username==request.session["Username"] or i.username=="all"]
    statuslist=[i.status for i in allobjects]
    data={
            "count":statuslist.count("unseen")}
    return JsonResponse(data)

def updateinfo(request):
    allobjects=mymodel.objects.get(username=request.session["Username"])
    data={"username":request.session["Username"],
    "fname":allobjects.first_name,
    "lname":allobjects.last_name,
    "email":allobjects.email,
    "faculty":allobjects.faculty,
    "batch":allobjects.batch,
    "image":allobjects.image,
    "phonenumber":allobjects.phonenumber,
    
    }
    return render(request, "updateinfo.html",data)

