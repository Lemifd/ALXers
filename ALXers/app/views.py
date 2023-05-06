from django.shortcuts import render
from datetime import datetime,timedelta
from django.http import HttpResponse,HttpResponseRedirect

from .models import User,Image
from time import sleep
from . import Q1
from .Q1 import *
from .add import title,title_list
from .form import DocumentForm
global signed
signed=False
ques_dic,_titles=title()[0],title_list

active=None
ranked={}
def cookie(request):
    global active
    try:
      nam=request.COOKIES['name']
    except:
       nam=""
    if not nam:
       active=User.objects.get(fname=nam)
    return active
       
      
def activeUser(email):
   global active
   active=User.objects.get(email=email)
   try:
     pic=active.photo.url.split('static/')[1]
   except:
      pic="user.png"
   return active,pic
def checkin():
   if active:
      return True
   else:
      return False
def getquestion(a):
   return ques_dic[str(a)]
def ranker():
    ranklist={}
    for i in User.objects.all():
        ranklist[i.fname]=i.solved
    rank=[]
    for name,solved in ranklist.items():
       rank.append(solved)
    rank.sort(reverse=True)
    return ranklist,rank
def getrank(user):
   rankk=ranker()[1]
   index=rankk.index(user.solved)
   return index+1
def home(request):
    ranklis=ranker()[0]
    global ranked
    ranked={}
    sort_solved=sorted(ranklis.values(),reverse=True)
    for i in range(min(len(sort_solved),10)):
       sort_solved[i]
       for key, value in ranklis.items():
           if value==sort_solved[i]:
              ranked[key]=value
    global active
    try:
      nam=request.COOKIES['name']
      active=User.objects.get(fname=nam)
    except:
       nam=None
       active=None
    male=len(User.objects.filter(gender="male"))
    female=len(User.objects.filter(gender="female"))
    tot_sol=0
    tot_sub=0
    for i in User.objects.all():
       tot_sol+=i.solved
    for i in User.objects.all():
       tot_sub+=i.submitted
   


       
    if active:
        response=render(request,'index.html',{"name":ranked.items(),"signed":checkin(),"user":active,"img":activeUser(active.email)[-1],"form":DocumentForm,"male":male,'female':female,'tot_sol':tot_sol,'tot_sub':tot_sub}) 
        return response
    return render(request,'index.html',{"name":ranked.items(),"signed":checkin(),"k":nam,"active":active,"form":DocumentForm,"male":male,'female':female,'tot_sol':tot_sol,'tot_sub':tot_sub}) 
def problems(request):
    try:
      nam=request.COOKIES['name']
      active=User.objects.get(fname=nam)
    except:
       nam=None
       active=None
    if active:
       return render(request,'problems.html',{"signed":checkin(),"user":active,"img":activeUser(active.email)})
    else:
        return render(request,'problems.html',{"signed":checkin()})      
def register(request):
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['password']
        gender=request.POST['gender']
        dob=request.POST['dob']
        phone=request.POST['tel']        

        new_user=User(fname=fname,lname=lname,email=email,password=password,age=dob,phone=phone,solved=0,submitted=0,gender=gender)
        new_user.save()
   #  return HttpResponseRedirect("/signin/")
        return render(request,'signin.html')
def profile(request):

    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        try:
            user=User.objects.get(email=email,password=password)
            global active
            active=user
            activeUser(email)
            user_rank=getrank(active)
            try:
               acceptance=100*active.solved/active.submitted
               acceptance= "{:.2f}".format(acceptance) 
            except:
               acceptance=0
            respose=render(request,'profile.html',{"user":user,"img":activeUser(user.email)[-1],'rank':user_rank,"signed":True,"acceptance":acceptance,"form":DocumentForm()})
            try:
               expiredate=datetime.now().date()+timedelta(days=2)
               respose.set_cookie(key="name",value=user.fname,expires=expiredate,secure=True)
               activeUser(email)
            except Exception as exc:
                return HttpResponse(f"please enable cookies {exc}")
            return respose
        except Exception as ex:
            return render(request,'signin.html',{"error":f"incorrect password or email","error":ex.__str__()})
    else:
      try:
        nam=request.COOKIES['name']
        active=User.objects.get(fname=nam)
      except:
        nam=None
        active=None
      if active:
            try:
               acceptance=100*active.solved/active.submitted
               acceptance= "{:.2f}".format(acceptance) 
            except:
               acceptance=0
         

            return render(request,'profile.html',{"signed":checkin(),"user":active,"img":activeUser(active.email)[-1],'rank':getrank(active),"acceptance":acceptance,"form":DocumentForm})
      else:
            return render(request,'signin.html',{"error":"Log in first"})
def signin(request):
    response=render(request,'signin.html')

    return response
def logout(request):
   response=render(request,'index.html',{"name":ranked.items(),"signed":False})
   response.delete_cookie(key="name")
   global active
   active=None
   global signed
   signed=False
   return response
def problems(request):
    try:
      nam=request.COOKIES['name']
      active=User.objects.get(fname=nam)
    except:
       nam=None
       active=None
    if active:
       signed=True
    else:
       signed=False
    run=""
    if request.method=="POST":
        try:
            run=request.POST['answer']
        except:
            run=""
        try:
            submit=request.POST['submit']
        except:
            submit=""
        
    if active:
       return render(request,'problems.html',{"run":run, "problems":ques_dic, "value":"def solutions()","signed":signed,"img":activeUser(active.email)[-1],"title":_titles})
    return render(request,'problems.html',{"run":run, "problems":ques_dic, "value":"Code goes here","signed":signed,"title":_titles})
def questions(request,id):
    try:
      nam=request.COOKIES['name']
      active=User.objects.get(fname=nam)
    except:
       nam=None
       active=None
    if active:
       signed=True
    else:
       signed=False
 
    run=""
    result=""
    corr=True
    value="def solution():"
    eva=getquestion(id)

          
          

    if request.method=="POST":
        if not active:
           return render(request,'problems.html',{"description":eva['desc'],"run":run,"error":"You must log in ","result":"","value":value, "problems":ques_dic,"signed":signed,"title":_titles})

        try:
            run=request.POST['answer']
        except:
            run=""
        try:
            submit=request.POST['submit']
        except:
            submit=""  
        if not run: value=run
        elif not submit: value=submit
  
        f=open("app/run.py","w")   
        f.write(run)
        f.close()
    
    
        try:
         if run:
            from .run import solution as func
    
    
            dis=len(eva['case'][0][0])
            if dis<=1:
                for inp, ans in  eva['case']:
                   got=func(inp[0])
                   if ans!=func(inp[0]):
                      corr=False
                      result=f"""
                      wrong answer
                      input:{inp[0][0]} and {inp[1][0]}
                      got answer:{got}
                      expected:{ans}
                      """
                      break
                   else:
                      result=f"""
                      correct
                      
                      input:{inp[0]} and 
                      got answer:{got}
                      expected:{ans}
                      """
                     
            else: 
                _inputs=len(eva['case'][0][0])
                if _inputs==2:
                 for inp,ans in eva['case']:
              
                  got= func(inp[0][0],inp[1][0])
                  if got != ans:
                    corr=False 
                    result=f"""
                      wrong answer
                      input:{[inp[x][0] for x in range(_inputs)]}
                      got answer:{got}
                      expected:{ans}
                      """
                    break
                  else:
                      result=f"""
                      correct
                      input:{inp[0][0]} and {inp[1][0]}
                      got answer:{got}
                      expected:{ans}
                      """
                elif _inputs==3:
                  for inp,ans in eva['case']:
                     got= func(inp[0][0],inp[1][0],inp[2][0])
                     if got != ans:
                        corr=False
                        result=f"""
                      wrong answer
                      input:{[inp[x][0] for x in range(_inputs)]}
                      got answer:{got}
                      expected:{ans}
                      """
                        break
                     else:
                      result=f"""
                      correct
                      input:{inp[0][0]} and {inp[1][0]}
                  got answer:{got}
              expected:{ans}
            """
         if corr: 
            active.solved=active.solved+1
            active.save()
         active.submitted+=1
         active.save()
         return render(request,'problems.html',{"description":eva['desc'],"run":run,"result":result,"got":corr,"value":value, "problems":ques_dic,"signed":signed,"title":_titles,"img":activeUser(active.email)[-1],'type':eva['type']})
        except Exception as err:
   
         return render(request,'problems.html',{"description":eva['desc'],"run":run,"error":err.__str__(),"result":"","value":value, "problems":ques_dic,"signed":signed,"img":activeUser(active.email)[-1],"title":_titles,'type':eva['type']})
    else:
         if active:
            img=activeUser(active.email)[-1]
         else:
            img=None

         return render(request,'problems.html',{"description":eva['desc'],"value":value, "problems":ques_dic,"signed":signed,"title":_titles,"img":img,'type':eva['type']})
def add(request):

   if request.method=="POST":
      form=DocumentForm(data=None,files=request.FILES)
      if form.is_valid():
         form.save()
         obj=form.instance
         photo=obj.photo.url
      else:
        
        return HttpResponse(f'not validated {form} and {form.full_clean()}')
         
   
   return render(request,'add.html',{"form":DocumentForm,"photo":photo})
def uploads(request):
   try:
      nam=request.COOKIES['name']
      active=User.objects.get(fname=nam)
   except:
       nam=None
       active=None
   if active:
       signed=True
   else:
       signed=False
   form=DocumentForm(data=request.POST,files=request.FILES)
   if form.is_valid():
         form.save()
         obj=form.instance
         phot=obj.photo.url
         active.photo=phot

   else:
         return HttpResponse('not validated')
      

   return HttpResponseRedirect('/profile/')
       
 
        

 

   