from django.contrib import admin
from portal.models import Person,Work,Assignment,Course,Announcements,Chat

# Register your models here.
admin.site.register(Person)
admin.site.register(Chat)
admin.site.register(Course)
admin.site.register(Work)
admin.site.register(Assignment)
admin.site.register(Announcements)