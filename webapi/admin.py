import sys
import json
import re
from django.contrib import admin
from webapi.models import User, Dokumentasi, DokumentasiKategori, CodeDocumentation, Plan



class user(admin.ModelAdmin): 
    if "runserver" in sys.argv:
        actions =list(filter(bool,["".join(re.findall("[a-zA-Z_]", i.name.replace(" ","_")))  for i in Plan.objects.all()]))  
        def detect_action(self, request, query, name):
            for i in Plan.objects.all():
                if "".join(re.findall("[a-zA-Z_]", i.name.replace(" ","_"))) == name:
                    query.plan_name = i.name
                    query.max_request = i.max_request
                    query.req_counter = 0
                    query.allow_ip = json.dumps(json.loads(query.allow_ip)[:i.max_ip])
                    query.max_ip = i.max_ip
                    query.req_counter = 0
                    query.save()
        for i in actions:
            print(i)
            exec("%s=lambda self, request, query_set:self.detect_action(request, query_set, \"%s\")"%(i,i))
    list_display = ['nama', 'email']
    search_field = ['nama', 'email']
    list_filter = ['email_verfied', 'plan_name']
    list_per_page = 8
    
class plan(admin.ModelAdmin):
    list_display = ['name']
    search_field = ['name', 'max_request']
    list_per_page = 8
class documentation(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['categori']
    search_field = ['title']
    list_per_page = 8
class category(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_field = ['name']
    list_per_page = 8
class code_documentation(admin.ModelAdmin):
    list_display = ['api_name', 'language']
    search_field = ['language']
    list_filter = ['api_name','language']
    list_per_page = 8

admin.site.register(User, user)
admin.site.register(Dokumentasi, documentation)
admin.site.register(DokumentasiKategori, category)
admin.site.register(CodeDocumentation, code_documentation)
admin.site.register(Plan, plan)
# Register your models here.
