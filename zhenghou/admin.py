from django.contrib import admin

# Register your models here.
from .models import RawInfo

class RawinfoAdmin(admin.ModelAdmin):
  pass

admin.site.register(RawInfo, RawinfoAdmin)
