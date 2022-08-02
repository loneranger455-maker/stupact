from email.policy import default
from pathlib import Path
from datetime import datetime
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
from requests import delete, session
from dataforstupact.models import mymodel
from dataforstupact.models import stumartmodel,order_list,notifications,verifyrequest
from dataforstupact.forms import register_as_tutor
import requests,os,random
from django.contrib import messages
from django.core.paginator import Paginator
import uuid
from datetime import datetime, timezone
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
                symbol[2]=sym2
                symbol[3]=sym2                
            # elif faculty=="none" or batch=="none":
            #     error="Complete the select field"
            else:
                valuestobesaved=mymodel(email=email,password=password,username=username)
                valuestobesaved.save()
                valuestobesaved=notifications(username=username,notify="Welcome to stumart family.Hope you will like our services.",status="unseen")
                valuestobesaved.save()
                messages.add_message(request, messages.SUCCESS, "Account created sucessfully.You can log in to your account now.")
                return redirect("/login")
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
        messages.add_message(request, messages.ERROR, error)
    else:
        usernm=" "
    
    data={"error":"error",
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
    return render(request,"account.html",{"object":allobjects,"form":register_as_tutor
    })

def logout(request):
    request.session.flush()
    return redirect('/login')


#stumart rendering function
def stumartfunc(request):
    
    variable=stumartmodel.objects.all()
    user=mymodel.objects.get(username=request.session["Username"])
    
    if len(user.phonenumber)<10 or len(user.first_name)<3 or len(user.last_name)<3:
        check=1
    else:
        check=0
    data=list()

    if request.method=="POST":
        value=request.POST.get("search")
        allobj=[i.title for i in variable]
        allobj2=[i for i in allobj if i[0:len(value)]==value]
        variable=[i for i in variable if i.title in allobj2 ]
    for i in variable:
        if i.username!=request.session["Username"] and i.verify == False:
            temp=dict()
            temp["id"]=i.id
            temp["verify"]=mymodel.objects.get(username=i.username).verified
            temp["username"]=i.username
            temp["title"]=i.title
            temp["image"]=i.image 
            temp["price"]=i.price  
            temp["discription"]=i.details
            temp["time"]=timeagofunc(i.time)
            data.append(temp)
    paginate=Paginator(data,8)
    pageno=request.GET.get("page")
    page=paginate.get_page(pageno)
    data2={
        "itemlist":page,
        "category":"all",
        "check":check,
        "count":range(1,paginate.num_pages+1)
    }
    return render(request,"stumart.html",data2)

#for product menu in stumart

def productmenu(request,tabvalue):
    user=mymodel.objects.get(username=request.session["Username"])
    if len(user.phonenumber)<10 or len(user.first_name)<3 or len(user.last_name)<3:
        check=1
    else:
        check=0
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
                temp["id"]=i.id
                try:
                    status=order_list.objects.get(product=str(i.id))
                    temp["status"]=status.status
                except:
                    temp["status"]=""
                
                data.append(temp)
            paginate=Paginator(data,8)
            pageno=request.GET.get("page")
            page=paginate.get_page(pageno)
            data2={
            "itemlist":page,
            "check":check,
            "stucheck":"true",
            "count":range(1,paginate.num_pages+1)
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
            objforreward=mymodel.objects.get(username=request.session["Username"])
            objforreward.reward+=20
            objforreward.save()
            valuestobesaved=notifications(username=request.session["Username"],notify="You have obtained 20 reward points for placing the item.Keep going..",status="unseen")
            valuestobesaved.save()
            return redirect('/stumart')
        return render(request, "stumart/placeproduct.html",{"check":check,"rewards":user.reward,"verify":user.verified,"stucheck":"true"})
    elif tabvalue=="purchasehistory":
       
        allobjects=order_list.objects.all()
        buyerobjects=[i for i in allobjects if i.buyer==request.session["Username"] ]
        sellerobjects=[i for i in allobjects if i.seller==request.session["Username"] ]
        return render(request, "stumart/purchasehistory.html",{"buyer":buyerobjects,"seller":sellerobjects,"stucheck":"true"})
    else:
        return redirect('/stumart')

def productinfo(request,uniquevalue):
    data2=list()
    count=0;
    variable=stumartmodel.objects.all()
    variable=[i for i in variable]
    random.shuffle(variable)
    for i in variable:
        if i.username!=request.session["Username"] and i.id!=uniquevalue and i.verify == False:
            temp=dict()
            temp["id"]=i.id
            temp["verify"]=mymodel.objects.get(username=i.username).verified
            temp["username"]=i.username
            temp["title"]=i.title
            temp["image"]=i.image 
            temp["price"]=i.price  
            temp["discription"]=i.details
            temp["time"]=timeagofunc(i.time)
            data2.append(temp)
            count+=1
       
        if count==4:
            break 
    allobjects=stumartmodel.objects.get(id=uniquevalue)
    time=timeagofunc(allobjects.time)
    verify=mymodel.objects.get(username=allobjects.username).verified
    data={"object":allobjects,
    "verifycheck":verify,
    "time":time,
    "itemlist":data2,
    "stucheck":"true"
    }
    return render(request,"stumart/productinfo.html",data)
#for ordering product
def orderproduct(request,uniquevalue):
    allobjects=stumartmodel.objects.get(id=uniquevalue)
    myobject=mymodel.objects.get(username=request.session["Username"])
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
            save2=order_list(first_name=fname,last_name=lname,phonenumber=phonenumber,region=region,buyer=request.session["Username"],seller=allobjects.username,product=str(allobjects.id),delivery_charge=disc,price=allobjects.price,status="Order Verified",title=allobjects.title)
            save2.save()
            save2=stumartmodel.objects.get(id=int(uniquevalue))
            save2.verify=True
            save2.save()
            objforreward=mymodel.objects.get(username=request.session["Username"])
            objforreward.reward+=20
            objforreward.save()
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
    return render(request, "stumart/orderproduct.html",{"stucheck":"true","object":allobjects,"myobject":myobject})

#for notifications

def timeagofunc(time):
            today = datetime.now(timezone.utc)
            diff=today-time
            diff2=str(diff).split(",")
            if len(diff2)==1:
                diff=str(diff).split(':')
                diff=[i[0:2] for i in diff]
                times=["secs","mins","hrs"]
                ans=""
                try:
                    
                    diff.remove('0')
                    diff.remove('00')
                except:
                    pass
            
                ans=diff[0]+times[len(diff)-1]
            else:
                ans=diff2[0]
            return(ans)

def notification(request):
    timecounter=[]
    allobjects=notifications.objects.all()
    allobjects=[i for i in allobjects if i.username==request.session["Username"] or i.username=="all"]
    allobjects.reverse()
    notifylist=[]
    
    for i in allobjects:
            if i.status=="unseen":
                i.status="seen"
                i.save()
            
            notifylist.append(i.notify)
            timecounter.append(timeagofunc(i.time))
                   
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
    error=""
    allobjects=mymodel.objects.get(username=request.session["Username"])
    if request.method=="POST":
            username=request.POST.get("username") 
            email=request.POST.get("email")
            fname=request.POST.get("fname")
            lname=request.POST.get("lname")
            faculty=request.POST.get("faculty")
            batch=request.POST.get("batch")
            phonenumber=request.POST.get("phonenumber")
            allobjects3=mymodel.objects.all()
            allobjects1=[i.username for i in allobjects3]
            allobjects2=[i.email for i in allobjects3 ]
       
            # if len(fname)<3 or len(lname)<3:
            #     error="First and last name must be at least 3 characters long"
            if username in allobjects1 and username!=request.session["Username"]:
                error="Username already exist"
               
            elif email[-10:]!="@gmail.com":
                error="Email format is incorrect"
                
            elif email in allobjects2 and email!=request.session["email"]:
                error="User already registered from this email"
               
            elif len(username)<5:
                error="Username must be at least 5 characters long"
              
            elif len(phonenumber)<10:
                error="phone number is not correct"
            else:
                allobjects.first_name=fname
                allobjects.last_name=lname
                allobjects.phonenumber=phonenumber
                allobjects.email=email
                allobjects.username=username
                allobjects.faculty=faculty
                allobjects.batch=batch
                allobjects.save()
                return redirect("/user")

           
    data={"username":request.session["Username"],
    "fname":allobjects.first_name,
    "lname":allobjects.last_name,
    "email":allobjects.email,
    "faculty":allobjects.faculty,
    "batch":allobjects.batch,
    "image":allobjects.image,
    "phonenumber":allobjects.phonenumber,
    "error":error,
    
    }
    return render(request, "updateinfo.html",data)

def changepassword(request):
    sym1="✔"
    sym2="✘"
    allobjects=mymodel.objects.get(username=request.session["Username"])
    error=""
    symbol=["","",""]
    current=request.GET["current"]
    print(current)
    new=request.GET["new"]
    confirm=request.GET["confirm"]
    if allobjects.password!=current:
        error="old password is not correct"
        symbol[0]=sym2
    elif len(new)<8:
        error="password must be at least 8 characters long"
        symbol[0]=sym1
        symbol[1]=sym2
    elif new!=confirm:
        error="password dont match"
        symbol[0]=sym1
        symbol[1]=sym2
        symbol[2]=sym2
    else:
        allobjects.password=new
        allobjects.save()
        return redirect("/user")
    
    data={
        "error":error,
        "symbol":symbol
    }
    return JsonResponse(data)


def deleteproduct(request):
    productid=request.GET["id"]
    try:
        object1=stumartmodel.objects.get(id=productid)
        object1.delete()
    except:
        print(productid)
  
    return redirect("/stumart/myproducts")

def searchbycategory(request,category):
  
    variable=stumartmodel.objects.all()
    data=list()
    if request.method=="POST":
        value=request.POST.get("search")
        allobj=[i.title for i in variable]
        allobj2=[i for i in allobj if i[0:len(value)]==value]
        variable=[i for i in variable if i.title in allobj2 ]
    if category=="all":
        return redirect("/stumart")
    for i in variable:
        if i.username!=request.session["Username"] and i.category==category and i.verify == False:
            temp=dict()
            temp["verify"]=mymodel.objects.get(username=i.username).verified
            temp["id"]=i.id
            temp["username"]=i.username
            temp["title"]=i.title
            temp["image"]=i.image 
            temp["price"]=i.price  
            temp["discription"]=i.details
            temp["time"]=timeagofunc(i.time)
            data.append(temp)
        
    paginate=Paginator(data,8)
    pageno=request.GET.get("page")
    page=paginate.get_page(pageno)   
    data2={
        "itemlist":page,
        "category":category,
        "stucheck":"true",
        "count":range(1,paginate.num_pages+1)
    }
    
    return render(request,"stumart.html",data2)
    
def tutor(request):
    return render(request,"tutor.html")
def tutor_dashboard(request):
    return render(request, "tutor/tutor_register.html")
def verify(request):
    check=request.GET["check"]
    usernamelist2=verifyrequest.objects.all()
    usernamelist=[i.username for i in usernamelist2]
    print(check)
    if check=='0':
        fileval=request.GET["file"]
        verifyrequest(username=request.session["Username"],filevalue=fileval).save()
        data={"checker":"sent"}
        
    else:
        if request.session["Username"] in usernamelist:
            data={"checker":"present"}
        else:
            data={"checker":"notpresent"}
    return JsonResponse(data)