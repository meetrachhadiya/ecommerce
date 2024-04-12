from django.contrib import admin
from accounts.models import User, Address
# Register your models here.

class AddressAdmin(admin.StackedInline):
    model = Address

class UserAdmin(admin.ModelAdmin):
    inlines = [AddressAdmin]

admin.site.register(User, UserAdmin)
admin.site.register(Address)