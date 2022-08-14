from django.http import HttpResponse
from django.shortcuts import redirect, render
import os
from django.core.paginator import Paginator
from pathlib import Path
from .models import verifyrequest,mymodel,notifications,order_list,stumartmodel,queries
# Create your views here.

        # if len(title)<3 
        # value=stumart(title=title,image=image,category=category,price=price,details=discription,username=request.session["Username"])
        # value.save()

def adminstart(request):
        return redirect("/adminpanel/verifylist")
def adminpanel(request,menuvalue):
        if menuvalue=="verifylist":
                allobjects=verifyrequest.objects.all()
                return render(request,"admin/verify.html",{"objects":allobjects,"page":1})
        elif menuvalue=="orderlist":
                allobjects=order_list.objects.all()
                return render(request,"admin/order.html",{"objects":allobjects,"page":2})
        elif menuvalue=="allusers":
                allobjects=mymodel.objects.all()
                paginate=Paginator(allobjects,9)
                pageno=request.GET.get("page")
                page=paginate.get_page(pageno)  
                return render(request,"admin/users.html",{"objects":page,"page":0,"count":range(1,paginate.num_pages+1)})
        elif menuvalue=="messageslist":
                allobjects=queries.objects.all()
                return render(request,"admin/messages.html",{"objects":allobjects,"page":3})

def verifycontrol(request,value,username):
        objectget=verifyrequest.objects.get(username=username)
        if value==0: 
                var1=mymodel.objects.get(username=username)
                var1.verified=True
                var1.save()
                notifications(username=username,notify="Your account has been verified.Congrats on getting that cool badge on your name.").save()
                objectget.delete()
        elif value==1:
                notifications(username=username,notify="Your verify request has been declined.Please post file that clearify your identity.").save()
                objectget.delete()

        return redirect("/adminpanel")
def ordercontrol(request,value,productid):
        stumodal=stumartmodel.objects.get(id=productid)
        var1=order_list.objects.get(product=productid)
        if value==0: 
               
                var1.status="completed"
                var1.save()
                objforreward=mymodel.objects.get(username=var1.seller)
                objforreward.reward+=20
                objforreward.save()
                objforreward=mymodel.objects.get(username=var1.buyer)
                objforreward.reward+=20
                objforreward.save()
                valuestobesaved=notifications(username=var1.buyer,notify="You have obtained 20 reward points for the completing order.Keep going..",status="unseen")
                valuestobesaved.save()
                notifications(username=var1.seller,notify="Your item has been sold sucessfully").save()
                notifications(username=var1.seller,notify="You obtained 20 points for the sell.Great job.").save()
                temp=stumodal.image.url
                os.remove(str(Path(__file__).resolve().parent.parent)+temp)
                stumodal.delete()
        elif value==1:
        
                notifications(username=var1.buyer,notify="Sorry,your order has been cancelled.").save()
                var1.delete()
                stumodal.verify=False
                stumodal.save()
        return redirect("/adminpanel/orderlist")

def deletemessages(request,msgid):
        messageget=queries.objects.get(id=msgid)
        messageget.delete()
        return redirect("/adminpanel/messageslist")


        