from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import *
from django.db import connection

# Create your views here.
 ################################################################## 
def index(request):
    user=request.session.get('userid')
    ct=""
    if user:
        ct=mcart.objects.all().filter(userid=user).count()
        
    x=category.objects.all().order_by('-id')[0:6]
    pdata=myproduct.objects.all().order_by('-id')[0:7]
    mydict={"data":x,"prodata":pdata,"cart":ct}
    return render(request,'user/index.html',context=mydict)


################################################################### 


def about(request):
    user=request.session.get('userid')
    ct=""
    if user:
        ct=mcart.objects.all().filter(userid=user).count()
    return render(request,'user/aboutus.html',{"cart":ct})

#######################################################################

def product(request):
    user=request.session.get('userid')
    ct=""
    if user:
        ct=mcart.objects.all().filter(userid=user).count()
    return render(request,'user/product.html',{"cart":ct})

#######################################################################

def myorder(request):
    user=request.session.get('userid')
    ct=""
    if user:
        ct=mcart.objects.all().filter(userid=user).count()
    user=request.session.get('userid')
    oid=request.GET.get('oid')
    mydict={}
    if user:
        if user:
            if oid is not None:
                morder.objects.all().filter(id=oid).delete()
                return HttpResponse("<script>alert('your order hass been cancelled ...');location.href='/user/myorder/'</script>")

        cursor=connection.cursor()
        cursor.execute("select p.*,o.* from user_myproduct p,user_morder o where p.id=o.pid and o.userid='"+str(user)+"' and o.remarks='Pending'")
        pdata=cursor.fetchall()
        cursor.execute("select p.*,o.* from user_myproduct p,user_morder o where p.id=o.pid and o.userid='"+str(user)+"' and o.remarks='Delivered'")
        ddata=cursor.fetchall()
        mydict={"pdata":pdata,"cart":ct,"ddata":ddata}
    return render(request,'user/myorder.html',mydict)

#######################################################################

def enquiry(request):
    user=request.session.get('userid')
    ct=""
    if user:
        ct=mcart.objects.all().filter(userid=user).count()
    status=False
    if request.method=="POST":
        a=request.POST.get('name')
        b=request.POST.get('email')
        c=request.POST.get('mob')
        d=request.POST.get('msg')
        contactus(Name=a,Mobile=c,Email=b,Message=d).save()
        status=True

        #mdict={"Name":a,"Email":b,"Mobile":c,"Message":d}

    msg={"m":status,"cart":ct}
    return render(request,'user/enquiry.html',context=msg)

#######################################################################


def signup(request):
    
    if request.method=="POST":
        Name=request.POST.get('name')
        Email=request.POST.get('email')
        Mobile=request.POST.get('mob')
        Password=request.POST.get('passw')
        Address=request.POST.get('address')
        Picture=request.FILES.get('ppic')
        x=register.objects.all().filter(email=Email).count()
        if x==0:
            register(name=Name,email=Email,mob=Mobile,passw=Password,address=Address,ppic=Picture).save()
            return HttpResponse("<script>alert('you are successfully registerd');location.href='/user/home/'</script>")
        else:
            return HttpResponse("<script>alert('your email is already registerd');location.href='/user/signup/'</script>")
    return render(request,'user/signup.html')


#######################################################################

def myprofile(request):
    user=request.session.get('userid')
    x=""
    if user:
        if request.method=="POST":
            Name=request.POST.get('name')
            Mobile=request.POST.get('mob')
            Password=request.POST.get('passw')
            Address=request.POST.get('address')
            Picture=request.FILES.get('pic')
            register(email=user,name=Name,mob=Mobile,passw=Password,address=Address,ppic=Picture).save()
            return HttpResponse("<script>alert('your profile has been updated successfully');location.href='/user/myprofile/'</script>")

        x=register.objects.all().filter(email=user)
    d={"mdata":x}
    return render(request,'user/myprofile.html',d)

#######################################################################

def signin(request):
    if request.method=="POST":
        Email=request.POST.get('email')
        Passw=request.POST.get('passw')

        x=register.objects.all().filter(email=Email,passw=Passw).count()
        y=register.objects.all().filter(email=Email,passw=Passw)
        if x==1:
            request.session['userid']=Email
            request.session['userpic']=str(y[0].ppic)

            return HttpResponse("<script>alert('you are login');location.href='/user/home/'</script>")
        else:
            return HttpResponse("<script>alert('your userid or password is incorrect.... ');location.href='/user/signin/'</script>")


    return render(request,'user/signin.html')

#######################################################################

def mens(request):
    user=request.session.get('userid')
    ct=""
    if user:
        ct=mcart.objects.all().filter(userid=user).count()
    cid=request.GET.get('msg')
    cat=category.objects.all().order_by('-id')
    d=myproduct.objects.all().filter(mcategory=1)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=1,pcategory=cid)
    mydict={"cats":cat,"data":d,"a":cid,"cart":ct}
    return render(request,'user/mens.html',mydict)

#######################################################################

def womens(request):
    user=request.session.get('userid')
    ct=""
    if user:
        ct=mcart.objects.all().filter(userid=user).count()
    cid = request.GET.get('msg')
    cat = category.objects.all().order_by('-id')
    d = myproduct.objects.all().filter(mcategory=2)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=2, pcategory=cid)
    mydict = {"cats": cat, "data": d, "a": cid,"cart":ct}
    return render(request,'user/womens.html',mydict)

#######################################################################

def kids(request):
    user=request.session.get('userid')
    ct=""
    if user:
        ct=mcart.objects.all().filter(userid=user).count()
    cid = request.GET.get('msg')
    cat = category.objects.all().order_by('-id')
    d = myproduct.objects.all().filter(mcategory=3)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=3, pcategory=cid)
    mydict = {"cats": cat, "data": d, "a": cid,"cart":ct}
    return render(request,'user/kids.html',mydict)

#######################################################################


def viewproduct(request):
    user=request.session.get('userid')
    ct=""
    if user:
        ct=mcart.objects.all().filter(userid=user).count()
    a = request.GET.get('abc')
    x = myproduct.objects.all().filter(id=a)
    return render(request, 'user/viewproduct.html', {"pdata": x,"cart":ct})

#######################################################################

def signout(request):
    if request.session.get('userid'):
        del request.session['userid']
    return HttpResponse("<script>alert('You are signed out');location.href='/user/home/'</script>")

#######################################################################

def myordr(request):
    user=request.session.get('userid')
    pid=request.GET.get('msg')
    if user:
        if pid is not None:
            morder(userid=user,pid=pid,remarks="Pending",odate=datetime.now().date(),status=True).save()
            return HttpResponse("<script>alert('your order confirmed');location.href='/user/index/'</script>")
    else:
        return HttpResponse("<script>alert('you have to login first');location.href='/user/signin/'</script>")
    return render(request,"user/myordr.html")

#######################################################################

def mycart(request):
    p=request.GET.get('pid')
    user=request.session.get('userid')
    if user:
        if p is not None:
            mcart(userid=user,pid=p,cdate=datetime.now().date,status=True).save()
            return HttpResponse("<script>alert('your item has been selected successfully');location.href='/user/index/'</script>")

    else:
        return HttpResponse("<script>alert('You have to login First');location.href='/user/signin/'</script>")
    return render(request,'user/mcart.html')

#######################################################################

def showcart(request): 
    user=request.session.get('userid')
    md={}
    a=request.GET.get('msg')
    cid=request.GET.get('cid')
    pid=request.GET.get('pid')
    if user:
        if a is not None:
            mcart.objects.all().filter(id=a).delete()
            return HttpResponse("<script>alert('your item is deleted from cart');location.href='/user/showcart/'</script>")
        elif pid is not None:
            mcart.objects.all().filter(id=cid).delete()
            morder(userid=user,pid=pid,remarks="Pending",status=True,odate=datetime.now().date()).save()
            return HttpResponse("<script>alert('Your order has been successfully');location.href='/user/myorder/'</script>")
        cursor=connection.cursor()
        cursor.execute("select p.*,c.* from user_myproduct p,user_mcart c where p.id=c.pid and c.userid='"+str(user)+"'" )
        cdata=cursor.fetchall()
        md={"cdata":cdata}
    return render(request,'user/showcart.html',md)

#######################################################################

def cpdetail(request):
    c=request.GET.get('cid')
    p=myproduct.objects.all().filter(pcategory=c)
    
    return render(request,'user/cpdetail.html',{"pdata":p})
    
#######################################################################
def intro(request):
    return render(request,'user/intro.html')