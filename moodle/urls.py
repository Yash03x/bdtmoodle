"""moodle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.db.models.fields.related import RECURSIVE_RELATIONSHIP_CONSTANT
from django.urls import path
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView
from portal import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name ='home'),
    path('signup/',views.register,name='signup'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('update/',views.secure_update,name='pass_update'),
    path('update/course_page/',RedirectView.as_view(url='/course_page/')),
    path('signup/signup/', RedirectView.as_view(url='/signup/')),
    path('signup/login/', RedirectView.as_view(url='/login/')),
    path('login/login/', RedirectView.as_view(url='/login/')),
    path('login/signup/', RedirectView.as_view(url='/signup/')),
    path('logout/login/',RedirectView.as_view(url='/login/')),
    path('course_page/logout/',RedirectView.as_view(url='/logout/')),
    path('course_page/login/',RedirectView.as_view(url='/course_page/')),
    path('create_work/logout/',RedirectView.as_view(url='/logout/')),
    path('create_course/logout/',RedirectView.as_view(url='/logout/')),
    path('logout/signup/',RedirectView.as_view(url='/signup/')),
    path('create_work/',views.create,name='create_work'),
    path('create_course/',views.create_course,name='create_course'),
    path('login/create_work/course_page/',RedirectView.as_view(url='/course_page/')),
    path('login/create_course/course_page/',RedirectView.as_view(url='/course_page/')),
    path('course_page/',views.course,name='course_page'),
    path('course_page/course_page/',RedirectView.as_view(url='/course_page/')),
    path('login/course_page/',RedirectView.as_view(url='/course_page/')), 
    path('create_work/course_page/',RedirectView.as_view(url='/course_page/')),
    path('create_course/course_page/',RedirectView.as_view(url='/course_page/')),
    path('course_page/create_course/',RedirectView.as_view(url='/create_course/')),
    path('course_page/chats/',views.chats,name='chats'),
    path('course_page/todo/',views.todo,name='todo'),
    path('course_page/chats/<str:item>/',views.dm,name='dm'),
    path('course_page/<str:item>/course_chat/',views.course_chat,name='course_chat'),
    #path('course_page/<str:item>/statistics/',views.statistics,name='statistics'), 
    #path('course_page/<str:item>/grades/',views.grades,name='grades'),
    path('course_page/<str:item>/evaluate_work/logout/',RedirectView.as_view(url='/logout/')),
    path('course_page/<str:item>/evaluate_work/course_page/',RedirectView.as_view(url='/course_page/')),
    path('course_page/<str:item>/evaluate_work/',views.select_work,name='evaluate_work'),
    path('course_page/<str:item>/evaluate_work/<str:wrk>/graded/',views.submit_graded, name='graded'),
    path('course_page/<str:item>/evaluate_work/<str:wrk>/grader/',views.submit_grader, name='grader'),
    path('course_page/<str:item>/evaluate_work/<str:wrk>/<str:asn>/',views.feedback, name='feedback'),   
    path('course_page/<str:item>/evaluate_work/<str:wrk>/',views.evaluate, name='evaluation'),
    path('course_page/<str:item>/',views.enter_course, name='enter_course'),
    path('course_page/<str:item>/create_work/',views.create, name='create_work'),
    path('course_page/<str:item>/members/',views.members, name='members'),
    path('course_page/<str:item>/members/add_ta/',views.add_ta, name='add_TA'),
    path('course_page/<str:item>/members/remove_ta/',views.remove_ta, name='remove_TA'),
    path('course_page/<str:item>/members/add_stud/',views.add_stud, name='add_stud'),
    path('course_page/<str:item>/members/remove_stud/',views.remove_stud, name='remove_stud'),
    #path('course_page/<str:item>/members/<str:abc>/<str:xyz>/',views.members, name='members'),
    path('course_page/<str:item>/announce/',views.announce, name='announce'),  
    path('course_page/<str:item>/<str:wrk>/',views.submit, name='submission'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

