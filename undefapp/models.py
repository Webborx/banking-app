from django.contrib.auth.models import User
from django.db import models
import random
from django.utils import timezone
from decimal import Decimal

# Create your models here

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Phone_number = models.CharField(max_length=500, null=True)
    middle_name = models.CharField(max_length=500, null=True)
    Recent_address = models.CharField(max_length=500, null=True)
    Previous_address = models.CharField(max_length=500, null=True)
    annual_income = models.CharField(max_length=500, null=True)
    Average_income = models.CharField(max_length=500, null=True)
    date_of_birth = models.CharField(max_length=500, null=True)
    social_security = models.CharField(max_length=500, null=True)
    Last_employer= models.CharField( max_length = 500, null=True)
    Job_role= models.CharField( max_length =500, null = True)
    account_number = models.CharField(max_length=20)
    routing_number = models.CharField(max_length=20)
    is_frozen = models.BooleanField(default=False)  # New field
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)



    def __str__(self):
        return f"{self.user.username}'s profile"
    
    
class Uploadpicture(models.Model):
    DL= models.FileField(upload_to="DL_file/",null=True)
    SSN= models.FileField(upload_to="SSN_file/", null=True)
    W2= models.FileField(upload_to="W2_file/", null=True)
    ref= models.CharField(max_length=500, null=True)







class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
        ('transfer', 'Transfer'),
        ('deposit', 'Deposit'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(null=True, blank=True)
    date = date = models.DateTimeField(default=timezone.now) 
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_transactions')


    # for fake transaction bill pay
    recipient_account_number=models.CharField(max_length=30, blank=True,null=True)
    recipient_routing_number=models.CharField(max_length=30, blank=True,null=True)
    recipient_bank_name=models.CharField(max_length=100, blank=True,null=True)

    

    def save(self, *args, **kwargs):
     if self.pk:  # means it's an update
        old_status = Transaction.objects.get(pk=self.pk).status
     else:
        old_status = None

     super().save(*args, **kwargs)

    # If it's newly processed
     if self.status == 'processed' and old_status != 'processed':
        profile = self.user.profile
        amount_decimal = Decimal(str(self.amount))
        is_new = self.pk is None  # Only adjust balance on first save
        super().save(*args, **kwargs)

        if is_new and self.status == 'processed':
            profile = self.user.profile

        if self.transaction_type in ['deposit', 'credit']:
            profile.account_balance += amount_decimal
        elif self.transaction_type in ['debit', 'transfer']:
            profile.account_balance -= amount_decimal

        profile.save()
    def __str__(self):
        return f"{self.user.username} | {self.transaction_type.upper()} | ${self.amount} | {self.status}"

    # def save(self, *args, **kwargs):
    #  old_status = None
    #  if self.pk:  # Only if it's an update
    #     old_status = Transaction.objects.filter(pk=self.pk).values_list('status', flat=True).first()

    #  super().save(*args, **kwargs)  # Save first so self has the latest values

    # # Only update balance when status changes to 'processed'
    #  if self.status == 'processed' and old_status != 'processed':
    #     profile = self.user.profile
    #     amount_decimal = Decimal(str(self.amount))

    #     if self.transaction_type in ['deposit', 'credit']:
    #         profile.account_balance += amount_decimal
    #     elif self.transaction_type in ['debit', 'transfer']:
    #         profile.account_balance -= amount_decimal

    #     profile.save()

    # def __str__(self):
    #     return f"{self.user.username} | {self.transaction_type.upper()} | ${self.amount} | {self.status}"


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=20)
    number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=[("Active", "Active"), ("Locked", "Locked")])
    # cvv = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.user.username} - {self.card_type}"
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering=["-created_at"]

    def __str__(self):
        return f"To: {self.user.username} - {self.message[:40]}"



    
