from django.contrib import admin
from .models import User,Items,Canteen,Order

# Change admin site titles
admin.site.site_header = "CanKiet Admin Dashboard"
admin.site.site_title = "CanKiet Admin"
admin.site.index_title = "Welcome to the Cankiet Dashboard"


# Register your models here.
admin.site.register(User)
admin.site.register(Items)
admin.site.register(Canteen)
admin.site.register(Order)


