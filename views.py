from django.shortcuts import *
from django.http import *
from app1.models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

# Create your views here.
def signup1(request):
    if request.method=='POST' and request.FILES['myfile']:
        firstname1=request.POST.get("firstname")
        lastname1=request.POST.get("lastname")
        email1=request.POST.get("email")
        password1=request.POST.get("passwd")
        dobd1=request.POST.get("dobd")
        dobm1=request.POST.get("dobm")
        doby1=request.POST.get("doby")
        gender1=request.POST.get("gender")
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)


        c=signup(firstname=firstname1, lastname=lastname1,displayimage=uploaded_file_url, emailid=email1,  password=password1, dobd=dobd1, dobm=dobm1,doby=doby1, gender=gender1)
        c.save()
        d  = login(emailid=email1,password=password1)
        d.save()
        return redirect("http://127.0.0.1:8000/dp")

    return render(request,'signup.html',{})


def login1(request):
    if request.method=='POST':
        email1=request.POST.get("email")
        password1=request.POST.get("pass")
        try:
            a = login.objects.get(emailid=email1,password=password1)
            request.session["name"] = a.emailid
            return redirect("http://127.0.0.1:8000/homepage")
        except:
            return  render(request,'login.html',{'error':"userid or password is incorrect"})



    else:
        return render(request,'login.html',{})

def homepage(request):
    try:
        name = request.session["name"]
        a = signup.objects.get(emailid=name)
        b=post.objects.all()

        return render(request,'homepage.html',{"obj":a,"posts":b})
    except:
        return redirect("http://127.0.0.1:8000/login")


def dp(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'displayp.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request,'displayp.html')
def addpost(request):
    if request.method=='POST'  and request.FILES['postimage']:
        name = request.session['name']
        a = signup.objects.get(emailid=name)
        userid1 = request.POST.get("userid")
        posttitle1 = request.POST.get("posttitle")
        location1 = request.POST.get("location")
        activity1 = request.POST.get("activity")
        myfile = request.FILES['postimage']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        p = post(userid=a,posttitle=posttitle1,postimage=uploaded_file_url,location=location1,activity=activity1)
        p.save()
    return render(request,'addpost.html',{})

def viewpost(request,id):
    a = post.objects.get(id=id)
    likedone=False
    no_of_likes = like.objects.filter(postid=a).count()
    comments = comment.objects.filter(postid=a)
    try:
        a1=like.objects.get(postid=id,userid=request.session["name"])
        print("Like")
        likedone=True
    except:
        pass
    return render(request,'viewpost.html',{"b":a,"like":likedone,"nol":no_of_likes,"coms":comments})

def like1(request,id):
    if request.method=="POST":
        ide = request.session['name']
        a = signup.objects.get(emailid=ide)
        b = post.objects.get(id=id)
        like(postid=b,userid=a).save()
        return redirect('http://127.0.0.1:8000/viewpost/'+str(id))

    return HttpResponse("Error ,cannot access this page")
def comment1(request,id):
    if request.method=="POST":
        ide=request.session["name"]
        a=signup.objects.get(emailid=ide)
        b=post.objects.get(id=id)
        com=request.POST.get("comment")
        comment(postid=b,userid=a,commenttext=com).save()
        return redirect('http://127.0.0.1:8000/viewpost/'+str(id))
    return HttpResponse("Error ,cannot access this page")

def addfriend(request):
    allUser = signup.objects.all()
    # print(a)
    b = signup.objects.get(emailid=request.session["name"])
    # c = friendslist.objects.filter(sender=b,reqstatus='1')
    # d = {}
    # for i in c:
    #     d[i.reciever.emailid] = i.reqstatus
    # for i in a:
    #     print(i)
    #     try:
    #         print(d[i.emailid])
    #     except:

    #         d[i.emailid]=0
    # print(d)
    accept = friendslist.objects.filter(reciever=b)
    # query = Q(sender=b)
    # query.add(Q(reciever=b), Q.OR)
    c = friendslist.objects.filter(Q(sender=b) | Q(reciever=b))

    l1 = []
    for i in c:
        if(i.reciever==b):
            l1.append(i.sender.emailid)
        else:
            l1.append(i.reciever.emailid)


    u_list = []
    for i in allUser:
        if(i.emailid not in l1 ):
            u_list.append(i)


    return render(request,'addfriend.html',{"friend":u_list,'accept':accept})
    # return render(request,'addfriend.html',{"friend":a,'dic':d,'accept':accept})

from json import loads
def requestsent(request):
    if request.method=="POST":
        a = ''
        for i in request.POST:
            a = loads(i).get('data')

        sender = signup.objects.get(emailid=request.session["name"])
        reciever = signup.objects.get(emailid=a)
        print(sender, reciever)
        friendslist(reciever=reciever,sender=sender,reqstatus = "1").save()
        # print(a)
        # print(b)

    return JsonResponse({'result': True})
def acceptrequest(request):
    if request.method=="POST":
        a = ''
        for i in request.POST:
            a = loads(i).get('data')
        print(a)
        sender = signup.objects.get(emailid=a)
        reciever = signup.objects.get(emailid=request.session["name"])
        b = friendslist.objects.get(sender=sender,reciever=reciever)
        b.reqstatus = 2
        b.save()
    return JsonResponse({'result': True})

def cancelrequest(request):
    if request.method=='POST':
        a = ''
        for i in request.POST:
            a = loads(i).get('data')
        print(a)
        sender = signup.objects.get(emailid=a)
        reciever = signup.objects.get(emailid=request.session["name"])
        friendslist.objects.get(sender=sender,reciever=reciever).delete()
    return JsonResponse({'result':True})

def showfriend(request):
    a = signup.objects.get(emailid=request.session["name"])
    b = friendslist.objects.filter(Q(sender=a) | Q(reciever=a),reqstatus=2)
    l1 = []
    for i in b:
        if(i.reciever==a):
            l1.append(i.sender)
        else:
            l1.append(i.reciever)

    return render(request,'showfriend.html',{"friend":l1})

def chatting(request):
    return HttpResponse(request,'chatting.html')
