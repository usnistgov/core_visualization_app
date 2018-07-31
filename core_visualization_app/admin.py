
from django.contrib import admin


admin_urls = [

]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
