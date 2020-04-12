from django.contrib import admin
from .models import (
	Profile,
)

class ProfileAdmin(admin.ModelAdmin):
    # Display custom fields in Django admin
    list_display = ('user','timestamp')
    readonly_fields = ["timestamp"]

admin.site.register(Profile,ProfileAdmin)