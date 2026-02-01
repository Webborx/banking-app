from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
# from .models import Profile, Transaction, Card, Notification
from django.contrib.auth.models import User
from django.utils.html import format_html
# Register your models here.


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'balance', 'account_number', 'routing_number', 'is_frozen')
#     list_editable = ('balance', 'account_number', 'routing_number', 'is_frozen')
#     search_fields = ('user__username', 'account_number')
#     list_filter = ('is_frozen', 'routing_number')



# class CustomUserAdmin(DefaultUserAdmin):
#     list_display=('username','email','first_name','last_name','is_staff')


# admin.site.unregister(User)
# admin.site.register(User,CustomUserAdmin)

# admin.site.register(Profile)
# admin.site.register(Uploadpicture)
# # admin.site.register(Notification)





# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'amount', 'transaction_type', 'status', 'date')
#     list_editable = ('status',)
#     search_fields = ('user__username', 'description')
#     list_filter = ('transaction_type', 'status', 'date')
#     readonly_fields = ('user', 'amount', 'transaction_type', 'description', 'date')
#     ordering=('-date',)

#     # Let admin add rejection reason only if rejected
#     def get_readonly_fields(self, request, obj=None):
#         ro_fields = super().get_readonly_fields(request, obj)
#         if obj and obj.status != 'rejected':
#             ro_fields = ro_fields + ('rejection_reason',)
#         return ro_fields

# # admin.site.register(Transaction, TransactionAdmin)
# admin.site.register( TransactionAdmin)





# @admin.register(Card)
# class CardAdmin(admin.ModelAdmin):
#     list_display = ('user', 'card_type', 'number', 'expiry_date', 'status')
#     list_editable = ('status',)
#     list_filter = ('card_type', 'status')
#     search_fields = ('user__username', 'number')


# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ('user', 'message', 'is_read', 'created_at')
#     list_filter = ('is_read', 'created_at')
#     search_fields = ('user__username', 'message')
#     ordering=('-timestamp',)
# admin.site.register(Notification, NotificationAdmin)





# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'account_number', 'routing_number')
#     list_editable = ('account_number', 'routing_number')
#     search_fields = ('user__username', 'account_number', 'routing_number')
#     list_filter = ('routing_number','is_frozen')

# admin.site.register(Profile, ProfileAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Uploadpicture, Transaction, Card, Notification

# Custom user admin
class CustomUserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Profile admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'routing_number','account_balance')
    list_editable = ('account_number', 'routing_number','account_balance')
    search_fields = ('user__username', 'account_number', 'routing_number')
    list_filter = ('routing_number', 'is_frozen')


# Upload picture
admin.site.register(Uploadpicture)


# Transaction admin
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'status', 'date')
    list_editable = ('status',)
    search_fields = ('user__username', 'description')
    list_filter = ('transaction_type', 'status', 'date')
    # readonly_fields = ('user', 'amount', 'transaction_type', 'description' )
    readonly_fields = ( 'rejection_reason',)
    ordering = ('-date',)

    def get_readonly_fields(self, request, obj=None):
        ro_fields = super().get_readonly_fields(request, obj)
        if obj and obj.status != 'rejected':
            ro_fields = ro_fields + ('rejection_reason',)
        return ro_fields


# Card admin
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_type', 'number', 'expiry_date', 'status')
    list_editable = ('status',)
    list_filter = ('card_type', 'status')
    search_fields = ('user__username', 'number')


# Notification admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)  # fixed from -timestamp
