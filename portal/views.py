from django.shortcuts import render,redirect
from .forms import RegistrationForm,codeForm,AssignmentForm,updatePass,feedbackForm,WorkForm,CourseForm,ChatSearchForm,OTP,OTP_update,grader_sh_Form,graded_csv_Form
from .mail import assign_notif,announce_notif,submit_notif,eval_notif,otp_notice
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Chat, Person,Work,Assignment,Course,Announcements,Graded,Grader_sh
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import pytz
import random
import pandas as pd
import json
import threading
import os
import subprocess

utc=pytz.UTC

def home(request):
    return render(request,'main_home.html')

def register(request):
    if(request.method=='POST'):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            x = form.save()
            if (not(Person.objects.filter(user = x).exists())):
                    a = Person(user = x)
                    a.save()
            return redirect('/login/')
        else:
            form=RegistrationForm()
            return render(request,'signup.html',{'form':form})
    else:
        form=RegistrationForm()
        return render(request,'signup.html',{'form':form})

def Login(request):
    if(request.method=='POST'):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            uname=form.cleaned_data['username']
            upass=form.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                if (not(Person.objects.filter(user = request.user).exists())):
                    a = Person(user = request.user)
                    a.save()
                #current = Person.objects.get(user = request.user)
                #works = []
                #for w in Work.objects.all():
                #    if w.owner == current.user.username:
                #        works.append(w)
                #all_works = Work.objects.all()
                return redirect('course_page/')
                #return render(request,'course_page.html',{'all_works':all_works, 'works':works})
                #return render(request,'course_page.html',{'Person':request.user})
        else:
            return redirect('login/')
    else:
        form=AuthenticationForm()
        return render(request,'login.html',{'form':form})


def course(request):
    if request.user.is_authenticated:
        if (not(Person.objects.filter(user = request.user).exists())):
                    a = Person(user = request.user)
                    a.save()
        current = Person.objects.get(user = request.user)
        if (request.method == 'POST'):
            form = codeForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data['Code']
                instance = code.split('.')
                if(current in Course.objects.get(name = instance[0]).students.all()):
                    path = '/course_page/'+instance[0]+'/'+instance[1]+'/'
                    return redirect(path)
                else:
                    path = '/course_page/'
                    return redirect(path)
            else:
                form = codeForm()
        else:
            form = codeForm()

        courses_under = []
        courses_enrolled = []
        prcnt = {}
        for c in Course.objects.all():
            if c.educator.user.username == current.user.username:
                courses_under.append(c)
            elif current in c.ta.all():
                courses_under.append(c)
            elif current in c.students.all():
                courses_enrolled.append(c)
                i = 0
                for w in c.work_set.all():
                    for a in w.assignment_set.all():
                        if(a.name == current.user.username):
                           i = i+1
                if(c.work_set.all().count()!=0):
                    prcnt[c.name] = str((i*100)/(c.work_set.all().count()))
                else:
                    prcnt[c.name] = str(100.0)
                print(prcnt)
            print(courses_enrolled)
        return render(request,'course_page.html',{'form':form, 'courses':courses_under, 'prcnt':prcnt}) #prcnt
    else:
        return redirect('login/')

def todo(request):
    current = Person.objects.get(user = request.user)
    eval = []
    attempt = []
    for c in Course.objects.all():
      if c.educator.user.username == current.user.username:
        if(Work.objects.all().count() != 0):
            for w in Work.objects.all():
                if w.crs.name == c.name:
                    for a in w.assignment_set.all():
                        if(a.obtained_marks == -1):
                            eval.append(w)
                            break 
      elif current in c.ta.all():
        if(Work.objects.all().count() != 0):
            for w in Work.objects.all():
                if w.crs.name == c.name:
                    for a in w.assignment_set.all():
                        if(a.obtained_marks == -1):
                            eval.append(w)
                            break 
      elif current in c.students.all():
        if(Work.objects.all().count() != 0):
            for w in c.work_set.all():
                if(w.deadline):
                    if(w.deadline < utc.localize(datetime.now()) ):
                        continue
                found = False
                for a in w.assignment_set.all():
                   if(a.name == current.user.username):
                       found = True
                       break
                if(found == False):
                    attempt.append(w)
    args = {'Person':current, 'eval':eval, 'attempt':attempt}
    return render(request,'todo.html',args)

def chats(request):
    active_chats = []
    for c in Chat.objects.all():
        if (c.end1.user.username == request.user.username):
            active_chats.append(c.end2.user.username)
        elif (c.end2.user.username == request.user.username):
            active_chats.append(c.end1.user.username)      
    if(request.method=="POST"):
        form=ChatSearchForm(request.POST)
        if form.is_valid():
            for c in Chat.objects.all():
                if ((c.end1.user.username == request.user.username and c.end2.user.username == form.cleaned_data['name']) or (c.end2.user.username == request.user.username and c.end1.user.username == form.cleaned_data['name'])):
                    path='/course_page/chats/'+form.cleaned_data['name']+'/'
                    return redirect(path)
            end_2 = Person.objects.get(user = request.user)
            for p in Person.objects.all():
                if p.user.username == form.cleaned_data['name']:
                    end_2 = p
            c = Chat(end1 = Person.objects.get(user = request.user), end2 = end_2)
            c.save()
            path = '/course_page/chats/'+form.cleaned_data['name']+'/'
            return redirect(path)
        else:
            form=ChatSearchForm()
            args={'form':form, 'active_chats':active_chats}
            return render(request,'chat_active.html',args)
    else:
        form=ChatSearchForm()
        args={'form':form, 'active_chats':active_chats}
        return render(request,'chat_active.html',args)

def dm(request, item):
    current = Person.objects.get(user = request.user)
    for c in Chat.objects.all():
        if ((c.end1.user.username == current.user.username and c.end2.user.username == item) or (c.end2.user.username == current.user.username and c.end1.user.username == item)):
            if(request.method=="POST"):
                if request.POST.get("chkvalue"):
                    temp = c.content+'\n'+current.user.username+': '+request.POST.get("chkvalue")
                    c.content = temp
                    c.save()
                    print(c.content)
                path = '/course_page/chats/'+item+'/'
                return redirect(path)        
            else:
                print(c.content)
                txt = c.content.split('\n')
                txt = txt[1:]
                return render(request,'dm.html',{'txt':txt, 'name':item})    
            


def create_course(request):
    if(request.method=="POST"):
        form=CourseForm(request.POST)
        if form.is_valid():
            ed = Person.objects.get(user = request.user)
            cs = Course(educator=ed,name=form.cleaned_data['name'],mem_ta_allowed=form.cleaned_data['Member_allowance_to_TA'],create_ta_allowed=form.cleaned_data['Creation_allowance_to_TA'])
            cs.save()
            args={'cs':cs}
            return render(request,'create_course.html',args)
        else:
            form=CourseForm()
            args={'form':form}
            return render(request,'c_course.html',args)
    else:
        form=CourseForm()
        args={'form':form}
        return render(request,'c_course.html',args)

def enter_course(request, item):
    current = Person.objects.get(user = request.user)
    c = Course.objects.get(name = item)
    if (request.method == 'POST'):
        form = codeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['Code']
            instance = code.split('.')
            if(current in c.students.all()):
                path = '/course_page/'+instance[0]+'/'+instance[1]+'/'
                return redirect(path)
            else:
                path = '/course_page/'+instance[0]+'/'
                return redirect(path) 
        else:
            form = codeForm()
    else:
        form = codeForm()
    flag = 0
    works = []
    announce = c.announcements_set.all()
    if c.educator.user.username == current.user.username:
        flag = 0
        if(Work.objects.all().count() != 0):
            for w in Work.objects.all():
                if w.crs.name == c.name:
                    for a in w.assignment_set.all():
                        if(a.obtained_marks == -1):
                            works.append(w)
                            break 
        args = {'c':c, 'Person':current, 'works':works, 'form':form, 'announce':announce}
        return render(request,'ed_look.html',args)
    elif current in c.ta.all():
        flag = 1
        if(Work.objects.all().count() != 0):
            for w in Work.objects.all():
                if w.crs.name == c.name:
                    for a in w.assignment_set.all():
                        if(a.obtained_marks == -1):
                            works.append(w)
                            break 
        args = {'c':c, 'Person':current, 'works':works, 'form':form, 'announce':announce}
        return render(request,'ta_look.html',args)
    else :
        flag = 2
        if(Work.objects.all().count() != 0):
            for w in Work.objects.all():
                if w.crs.name == c.name:
                    works.append(w)
        args = {'c':c, 'Person':current, 'works':works, 'form':form, 'announce':announce}
        return render(request,'stud_look.html',args)

#################################################
def statistics(request, item,wrk):
 #should pass data and name
  data=[['student name','marks']]
  p_data=[]
  dict={'max':0,'average':0,'min':0,'median':0}
  name=wrk
  if request.user.is_authenticated:
    for obj in Work.objects.all():
        if(obj.name==wrk):
            if(request.user.username==obj.crs.educator.user.username):
                for sub in obj.assignment_set.all():
                    data.append([sub.name,str(sub.obtained_marks)])
                    p_data.append([sub.name,float(sub.obtained_marks)])
                data_json=json.dumps(data)
                name_json=json.dumps(name)
                df=pd.DataFrame(p_data,columns=['student_name','marks'])
                dict['max']=df['marks'].max()
                dict['average']=df['marks'].mean()
                dict['min']=df['marks'].min()
                dict['median']=df['marks'].median()
                dict['std']=df['marks'].std()
                return render(request,'stats.html',{'item':item, 'wrk':wrk, 'data':data_json,'name':name_json,'dict':dict})
            break
    return redirect('/course_page/')
    

###############################################
def grades(request, item):
  if request.user.is_authenticated:
   dict1={}
   dict2={'total':0}
   p_tot=0
   data=[['id','marks','mean_marks','lowest_marks']]
   per=1
   for obj in Course.objects.all():
       if(obj.name==item):
           w_total=0
           for a in obj.work_set.all():
              if a!=None:
               w_total+=a.weightage*a.total_marks/100
               dict1[a.name]=0
               for b in a.assignment_set.all():
                   if(b.name==request.user.username):
                       if(b.obtained_marks==-1):
                           dict1[a.name]=0
                       else:
                           dict1[a.name]=b.obtained_marks*a.weightage
                           mean,low=fetch(a.name)
                           per_a=0
                           if(mean<=b.obtained_marks*a.weightage):
                               per_a=1
                           per=(per_a+per)*0.5
                           data.append([p_tot,b.obtained_marks*a.weightage,mean,low])
                           p_tot+=1
               dict2['total']+=dict1[a.name]
           if w_total!=0:
                for i in dict1.keys():
                        dict1[i]=dict1[i]/w_total
                dict2['total']=dict2['total']/w_total
           break
   data_json=json.dumps(data)
   if(per==0):
       per='alarming'
   elif(per>0.5):
       per='excellent'
   else:
       per='avarage'
   return render(request,'grade_page.html',{'name':item, 'd1':dict1,'d2':dict2,'data':data_json,'performance':per})


def overall_stats(request,item):
    data=[['id','mean','lowest']]
    tot=0
    if request.user.is_authenticated:
        for obj in Course.objects.all():
            if obj.name==item:
                if obj.educator.user.username==request.user.username:
                  for wrk in obj.work_set.all():
                      mean,low=fetch(wrk.name)
                      print(mean,low)
                      data.append([tot,mean,low])
                      tot+=1
                  data_json=json.dumps(data)
                  return render(request,'ov.html',{'name':item, 'data':data_json})
                
def fetch(wrk):
    mean=0
    low=2000
    tot=0
    for obj in Work.objects.all():
        if(obj.name==wrk):
            for j in obj.assignment_set.all():
               if j.obtained_marks!=-1:
                  mean+=j.obtained_marks*obj.weightage
                  tot+=1
                  if low>j.obtained_marks*obj.weightage:
                     low=j.obtained_marks*obj.weightage
            if(tot!=0):
                mean=mean/tot
            if low==2000:
                low=0
            return (mean,low)

def course_chat(request, item):
    current = Person.objects.get(user = request.user)
    c = Course.objects.get(name = item)
    ed_bool = False
    if(c.educator.user.username == current.user.username):
        ed_bool = True
    if(request.method=="POST"):
            if request.POST.get("chkvalue"):
                if(ed_bool == True and request.POST.get("chkvalue")=='DISABLE'):
                    c.chat_allowed = False
                if(ed_bool == True and request.POST.get("chkvalue")=='ENABLE'):
                    c.chat_allowed = True
                temp = c.chat_content+'\n'+current.user.username+': '+request.POST.get("chkvalue")
                c.chat_content = temp
                c.save() 
            path = '/course_page/'+item+'/course_chat/'
            return redirect(path)        
    else:
        txt = c.chat_content.split('\n')
        txt = txt[1:]
        return render(request,'course_forum.html',{'ed_bool':ed_bool, 'txt':txt, 'name':item, 'allowed':c.chat_allowed})    


def announce(request, item):
    c = Course.objects.get(name = item)
    if(request.method=="POST"):
        if request.POST.get("chkvalue"):
            a = Announcements(crs=c, content=request.POST.get("chkvalue"))
            a.save()
            #announce_notif(c.educator.user.username,c.educator.user.email,item,request.POST.get("chkvalue"))
            t = threading.Thread(target=announce_notif, args=(c.educator.user.username,c.educator.user.email,item,request.POST.get("chkvalue")))
            t.start()
            for i in c.ta.all():
                #announce_notif(i.user.username,i.user.email,item,request.POST.get("chkvalue"))
                t = threading.Thread(target=announce_notif, args=(i.user.username,i.user.email,item,request.POST.get("chkvalue")))
                t.start()
            for i in c.students.all():
                #announce_notif(i.user.username,i.user.email,item,request.POST.get("chkvalue"))
                t = threading.Thread(target=announce_notif, args=(i.user.username,i.user.email,item,request.POST.get("chkvalue")))
                t.start()
            path = '/course_page/'+item+'/'
            return redirect(path)         
    else:
        return render(request,'announce.html',{'item':item})    


def members(request, item):
    current = Person.objects.get(user = request.user)
    c = Course.objects.get(name = item)
    tas = c.ta.all()
    studs = c.students.all()
    return render(request,'mem.html',{'tas':tas, 'studs':studs, 'current':current, 'c':c})

def add_ta(request, item):
    c = Course.objects.get(name = item)        
    people = []
    for p in Person.objects.all():
        if ((p.user.username != c.educator.user.username)  and  (p not in c.ta.all())  and  (p not in c.students.all())):
            people.append(p)
    if(request.method=="POST"):
        if request.POST.get("chkvalue"):
            for p in people:
                if p.user.username == request.POST.get("chkvalue"):
                    c.ta.add(p)
                    break
        path = '/course_page/'+item+'/members/'
        return redirect(path)        
    else:
        return render(request,'add_ta.html',{'name':item, 'people':people})    

def remove_ta(request, item):
    c = Course.objects.get(name = item)
    people = []
    for p in Person.objects.all():
        if p in c.ta.all():
            people.append(p)
    if(request.method=="POST"):
        if request.POST.get("chkvalue"):
            for p in people:
                if p.user.username == request.POST.get("chkvalue"):
                    c.ta.remove(p)
                    break
        path = '/course_page/'+item+'/members/'
        return redirect(path)         
    else:
        return render(request,'remove_ta.html',{'name':item, 'people':people})  

def add_stud(request, item):
    c = Course.objects.get(name = item)
    people = []
    for p in Person.objects.all():
        if ((p.user.username != c.educator.user.username)  and  (p not in c.ta.all())  and  (p not in c.students.all())):
            people.append(p)
    if(request.method=="POST"):
        if request.POST.get("chkvalue"):
            for p in people:
                if p.user.username == request.POST.get("chkvalue"):
                    c.students.add(p)
                    break
        path = '/course_page/'+item+'/members/'
        return redirect(path)         
    else:
        return render(request,'add_stud.html',{'name':item, 'people':people}) 

def remove_stud(request, item):
    c = Course.objects.get(name = item)
    people = []
    for p in Person.objects.all():
        if p in c.students.all():
            people.append(p)
    if(request.method=="POST"):
        if request.POST.get("chkvalue"):
            for p in people:
                if p.user.username == request.POST.get("chkvalue"):
                    c.students.remove(p)
                    break
        path = '/course_page/'+item+'/members/'
        return redirect(path)         
    else:
        return render(request,'remove_stud.html',{'name':item, 'people':people})  

def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request,'main_home.html')
    else :
        return render(request,'main_home.html')

def create(request, item): 
    if(request.method=="POST"):
        form=WorkForm(request.POST)
        if form.is_valid():
            c = Course.objects.get(name = item)
            ################################################
            ass=Work(crs=c,name=form.cleaned_data['name'],total_marks=form.cleaned_data['total_marks'],deadline=form.cleaned_data['deadline'],weightage=form.cleaned_data['weightage_parameter'])
            ass.save()
            code = ass.crs.name + '.' + ass.name
            #assign_notif(c.educator.user.username,c.educator.user.email,code,0)
            t = threading.Thread(target=assign_notif, args=(c.educator.user.username,c.educator.user.email,code,0))
            t.start()
            for i in c.ta.all():
                #assign_notif(i.user.username,i.user.email,code,1)
                t = threading.Thread(target=assign_notif, args=(i.user.username,i.user.email,code,1))
                t.start()
            for i in c.students.all():
                #assign_notif(i.user.username,i.user.email,code,2)
                t = threading.Thread(target=assign_notif, args=(i.user.username,i.user.email,code,2))
                t.start()
            ################################################
            args={'c':c,'name':ass.name,'tot':ass.total_marks,'deadline':ass.deadline,'weight':ass.weightage}
            return render(request,'create_work.html',args)
        else:
            form=WorkForm()
            args={'form':form, 'name':item}
            return render(request,'c_work.html',args)
    else:
        form=WorkForm()
        args={'form':form, 'name':item}
        return render(request,'c_work.html',args)

def select_work(request, item):
    if(request.user.is_authenticated):
        current = Person.objects.get(user = request.user)
        c = Course.objects.get(name = item)
        works = c.work_set.all()
        return render(request,'select_work_page.html',{'name':item, 'works':works})
    else:
        form=AuthenticationForm()
        return render(request,'login.html',{'form':form})

def evaluate(request, item, wrk):
    if(request.user.is_authenticated):
        current = Person.objects.get(user = request.user)
        work_obj = Work.objects.get(name = wrk)
        assignments = work_obj.assignment_set.all()
        '''for a in Assignment.objects.all():
            if a.work == work_obj:
                assignments.append(a)'''
        return render(request,'evaluate.html',{'item':item, 'assignments':assignments, 'name':wrk})
    else:
        form=AuthenticationForm()
        return render(request,'login.html',{'form':form})
    
def user_update(old_name,new_name):
    for i in Work.objects.all():
        if i.owner==old_name:
            i.owner=new_name
            i.save()
    for i in Assignment.objects.all():
        if i.name==old_name:
            i.name=new_name
            i.save()
otp_obj=None

def secure_update(request,*args,**kwargs):
    global otp_obj
    if request.user.is_authenticated:
        if(request.method=='POST'):
            if(otp_obj!=None):
                form=OTP(request.POST)
                if form.is_valid():
                    if otp_obj.check(form.cleaned_data['otp_enter'])==-1:
                        return redirect('/course_page/')
                    elif otp_obj.check(form.cleaned_data['otp_enter'])==0:
                        otp_obj=None
                        return redirect('/course_page/')
                    elif otp_obj.check(form.cleaned_data['otp_enter'])==1:
                        form_m=updatePass({'username':request.user.username,'first_name':request.user.first_name,'last_name':request.user.last_name,'email':request.user.email})
                        otp_obj=None
                        return render(request,'update.html',{'current':request.user, 'form':form_m})
                else:
                    form=OTP()
                    return render(request,'otp.html',{'form':form})
            else:
                return redirect('/course_page/')
        else:
            otp_obj=OTP_update(random.randint(1111,9999))
            #otp_notice(request.user.username,request.user.email,otp_obj.otp_real)
            t = threading.Thread(target=otp_notice, args=(request.user.username,request.user.email,otp_obj.otp_real))
            t.start()
            form=OTP()
            return render(request,'otp.html',{'form':form})
    else:
        form=AuthenticationForm()
        return render(request,'login.html',{'form':form})
            
def grade_csv(request,work_name):
    pass

def update(request,*args,**kwargs):
    if request.user.is_authenticated:
        if(request.method=='POST'):
            form=updatePass(request.POST)
            if form.is_valid():
                user=authenticate(username=request.user.username,password=form.cleaned_data['old_password'])
                if user is not None:
                    user_update(request.user.username,form.cleaned_data['username'])
                    user.username=form.cleaned_data['username']
                    user.email=form.cleaned_data['email']
                    user.first_name=form.cleaned_data['first_name']
                    user.last_name=form.cleaned_data['last_name']
                    if form.data['password']:
                        user.set_password(form.cleaned_data['password'])
                        user.save()
                    user.save()
                return redirect('/course_page/')
            else:
                form=updatePass({'username':request.user.username,'first_name':request.user.first_name,'last_name':request.user.last_name,'email':request.user.email})
        else:
            form=updatePass({'username':request.user.username,'first_name':request.user.first_name,'last_name':request.user.last_name,'email':request.user.email})
        return render(request,'update.html',{'current':request.user, 'form':form})
    else:
        form=AuthenticationForm()
        return render(request,'login.html',{'form':form})
    

def submit_graded(request, item,wrk):
    if(request.method=='POST'):
        form=graded_csv_Form(request.POST,request.FILES)
        if form.is_valid():
            ass=form.save(commit=False)
            for w in Work.objects.all():
                if w.name==wrk:
                    ass.name=request.user.username
                    ass.work=w
                    ass.save()
                    status=False
                    feed_csv(w)
                    return render(request, 'csv_show.html',{'item':item, 'wrk':wrk, 'assign':ass, 'status':status})
        else:
            form=graded_csv_Form()
    else:
        if request.user.is_authenticated:
            current = Person.objects.get(user = request.user)
        try:
            work_obj = Work.objects.get(name = wrk)
        except:
            work_obj=None
        for a in work_obj.graded_set.all():
            if (a.name == request.user.username):
                status = False
                return render(request, 'csv_show.html',{'item':item, 'wrk':wrk, 'assign':a, 'status':status})
        form = graded_csv_Form()
        return render(request, 'csv_submit.html', {'item':item, 'wrk':wrk, 'form':form, 'work':work_obj})

                    

def submit_grader(request, item,wrk):
    if(request.method=='POST'):
        form=grader_sh_Form(request.POST,request.FILES)
        if form.is_valid():
            ass=form.save(commit=False)
            for w in Work.objects.all():
                if w.name==wrk:
                    ass.name=request.user.username
                    ass.work=w
                    ass.save()
                    status=False
                    return render(request, 'csv_show.html',{'item':item, 'wrk':wrk, 'assign':ass, 'status':status})
        else:
            form = grader_sh_Form()
    else:
        if request.user.is_authenticated:
            current = Person.objects.get(user = request.user)
        try:
            work_obj = Work.objects.get(name = wrk)
        except:
            work_obj=None
        for a in work_obj.grader_sh_set.all():
            if (a.name == request.user.username):
                status = False
                return render(request, 'csv_show.html',{'item':item, 'wrk':wrk, 'assign':a, 'status':status})
        form = grader_sh_Form()
        return render(request, 'csv_submit.html', {'item':item, 'wrk':wrk, 'form':form, 'work':work_obj})

def submit(request, item, wrk):
    if (request.method == 'POST'):
        #print('yes')
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            ass = form.save(commit=False)
            for w in Work.objects.all():
                if w.name == wrk:
                    ass.name = request.user.username
                    ass.work = w
                    ass.obtained_marks = -1
                    ass.save()
                    #submit_notif(request.user.username,request.user.email,wrk,w.crs.name)
                    t = threading.Thread(target=submit_notif, args=(request.user.username,request.user.email,wrk,w.crs.name))
                    t.start()
                    status = False
                    return render(request, 'show.html',{'item':item, 'wrk':wrk, 'assign':ass, 'status':status})
        else:
            form = AssignmentForm()
    else:
        if request.user.is_authenticated:
            current = Person.objects.get(user = request.user)
        try:
            work_obj = Work.objects.get(name = wrk)
        except:
            work_obj=None
            return redirect('/course_page/')
        for a in work_obj.assignment_set.all():
            if (a.name == request.user.username):
                status = True
                if(a.obtained_marks == -1):
                    status = False
                return render(request, 'show.html',{'item':item, 'wrk':wrk, 'assign':a, 'status':status})
        form = AssignmentForm()
        dead = False
        if(work_obj.deadline):
            dead = work_obj.deadline < utc.localize(datetime.now()) 
        return render(request, 'submit.html', {'item':item, 'wrk':wrk, 'form':form, 'work':work_obj, 'dead_bool':dead})

def feedback(request, item, wrk, asn):
    if (request.method == 'POST'):
        form = feedbackForm(request.POST)        
        work_obj = Work.objects.get(name = wrk)
        for a in Assignment.objects.all():
            if (a.work == work_obj and a.name == asn):
                if form.is_valid():
                    a.obtained_marks = form.cleaned_data['Marks_Obtained']
                    a.save()
                    for p in Person.objects.all():
                        if(p.user.username == a.name):
                            #eval_notif(p.user.username,p.user.email,wrk,work_obj.crs.name)
                            t = threading.Thread(target=eval_notif, args=(p.user.username,p.user.email,wrk,work_obj.crs.name))
                            t.start()
                    status = True
                    return render(request, 'give_feedback.html',{'item':item, 'wrk':wrk, 'assign':a, 'status':status})
                else:
                    form = feedbackForm()
                    status = False
                    return render(request, 'give_feedback.html',{'item':item, 'wrk':wrk, 'assign':a, 'status':status, 'form':form})
    else:
        current = Person.objects.get(user = request.user)
        work_obj = Work.objects.get(name = wrk)
        for a in Assignment.objects.all():
            if (a.work == work_obj and a.name == asn):
                status = True
                if(a.obtained_marks == -1):
                    status = False
                    form = feedbackForm()
                    return render(request, 'give_feedback.html',{'item':item, 'wrk':wrk, 'assign':a, 'form':form, 'status':status})
                return render(request, 'give_feedback.html',{'item':item, 'wrk':wrk, 'assign':a, 'status':status})

def feed_csv(wrk):
  for obj in Graded.objects.all():
      if(obj.work.name==wrk.name):
           data=pd.read_csv('.'+'/'+obj.submission.url)
           cols=data.columns
           for i in range(data[cols[0]].size):
               for j in wrk.assignment_set.all():
                   if(j.name==data[cols[0]][i]):
                        j.obtained_marks=data[cols[1]][i]
                        j.save()
                        for p in Person.objects.all():
                            if(p.user.username == j.name):
                                #eval_notif(p.user.username,p.user.email,wrk,work_obj.crs.name)
                                t = threading.Thread(target=eval_notif, args=(p.user.username,p.user.email,wrk.name,wrk.crs.name))
                                t.start()

def feed_grader(wrk):
    for obj in Grader_sh.objects.all():
      if(obj.work.name==wrk.name):
          for a in wrk.assignment_set.all():
            a1 = '.'+'/'+'media'+'/'+a.path
            a2 = (a.submission.url).split('/')[-1]
            a3 = a.name
            a4 = wrk.name
            a5 = wrk.total_marks
            a6 = len(a1.split('/'))
            st=os.stat('/'+'media'+'/'+obj.path+(obj.submission.url).split('/')[-1])
            os.chmod('/'+'media'+'/'+obj.path+(obj.submission.url).split('/')[-1],st.st_mode | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)
            print(st.st_mode)
            subprocess.call(['./'+'media'+'/'+obj.path+(obj.submission.url).split('/')[-1], a1, a2, a3, a4, str(a5), str(a6)])
            data=pd.read_csv('.'+'/'+'media'+'/'+a.path+a4+'.csv')
            cols=data.columns
            for i in range(data[cols[0]].size):
                for j in wrk.assignment_set.all():
                    if(j.name==data[cols[0]][i]):
                        j.obtained_marks=data[cols[1]][i]
                        j.save()
                        break


  
  



  
  
