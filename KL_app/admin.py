from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display=('username','first_name','last_name')

class CollectionAdmin(admin.ModelAdmin):
    list_display=('nom_collection','active')

class ModeleAdmin(admin.ModelAdmin):
    list_display=('nom_modele','collection','disponible')

class AccessoireAdmin(admin.ModelAdmin):
    list_display=('nom_accessoire','collection','disponible')



class CommandeModeleAdmin(admin.ModelAdmin):
     list_display=('date_cmd','client','modele','confirme')

class CommandeAccessoireAdmin(admin.ModelAdmin):
    list_display=('date_cmd','client','accessoire','confirme')

admin.site.register(User,UserAdmin)
admin.site.register(Collection,CollectionAdmin)
admin.site.register(Modele,ModeleAdmin)
admin.site.register(Accessoire,AccessoireAdmin)
admin.site.register(Commandemodele,CommandeModeleAdmin)
admin.site.register(Commandeaccessoire,CommandeAccessoireAdmin)
