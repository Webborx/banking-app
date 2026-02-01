from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .forms import UserRegisterForm,Uploadpicture,ProfileForm, PayBillForm
# from . models import Profile
import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Card, Transaction,Notification,Profile

# Create your views here.

@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
    profile=Profile.objects.get(user=request.user)
    cards = Card.objects.filter(user=request.user)
    
    return render(request,'dashboard.html',{"profile":profile,"transactions":transactions,
                                            'cards': cards, "notifications":notifs})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # replace with your dashboard URL name
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')



def register(request):
    if request.method =="POST":
        user_form=UserRegisterForm(request.POST)
        profile_form= ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()

            return redirect('register2')
    else:
        user_form=UserRegisterForm()
        profile_form=ProfileForm()

    return render(request,"register.html",{'user_form':user_form,
                                           'profile_form':profile_form})
        

    

    # return HttpResponse(template.render( {"forrm":form}))
            

def first(request):

    # lastFund = UNFUNDS.objects.last()
    # return render(req, 'pages/first.html', {'Fund': lastFund})
    latestFund = Profile.objects.latest('id')
    randomnumber=request.session.get('randomnumber','N/A')
    return render(request, 'first.html', {'Fund': latestFund,
                                          'randomnumber':randomnumber})



def viewallfunds(request):
    allFunds = Profile.objects.all()
    return render(request, 'pages/allFunds.html', {'Fund': allFunds})



def register2(request):
    form=Uploadpicture()
    if request.method=="POST":
        randomnumber=randomnumbergen()[0]
        post_data=request.POST.copy()
        post_data["ref"]=randomnumber
        form=Uploadpicture(post_data,request.FILES)
       
                         


        if form.is_valid():
            form.save()
            request.session["randomnumber"]=randomnumber
            return redirect("firsturl")
        else:
            print("\n\n\n form not saved\n\n\n")
            print(f"\n{request.POST}\n")
            print(form.errors)

    return render (request,"register2.html",{"form":form})






def randomnumbergen():
    generated_numbers = []
    for _ in range(1):
        second = str(random.randint(1, 888)).zfill(3)
        last = str(random.randint(1, 9998)).zfill(4)
        first= 1111
        
        # Ensure the number doesn't end with repetitive patterns
        while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
            last = str(random.randint(1, 9998)).zfill(4)
        
        generated_numbers.append(f"{first}{second}{last}")
    
    return generated_numbers







@login_required
def lock_card(request, card_id):
    card = get_object_or_404(Card, id=card_id, user=request.user)
    card.status = "Locked"
    card.save()
    return redirect('/dashboard/?toast=Card locked successfully')

@login_required
def unlock_card(request, card_id):
    card = get_object_or_404(Card, id=card_id, user=request.user)
    card.status = "Active"
    card.save()
    return redirect('/dashboard/?toast=Card unlocked successfully')




@login_required
def deposit_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        Transaction.objects.create(
            user=request.user,
            amount=amount,
            transaction_type='deposit',
            description=description,
            status='pending',  # Will wait for admin approval
        )
        return render(request, 'deposit.html', {'success': True})

    return render(request, 'deposit.html')


@login_required
def user_notifications(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
    # Mark all as read
    notifs.update(is_read=True)

    return render(request, 'notifications.html', {'notifications': notifs})



@login_required
def transfer_money(request):
    users = User.objects.exclude(id=request.user.id)  # prevent sending to self

    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        amount = float(request.POST.get('amount'))
        description = request.POST.get('description')

        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            messages.error(request, "Recipient not found.")
            return redirect('transfer')

        # Create transaction for sender (debit)
        Transaction.objects.create(
            user=request.user,
            recipient=recipient,
        
            amount=amount,
            transaction_type='transfer',
            description=description,
            status='processed',
        )

        # Create transaction for recipient (credit)
        Transaction.objects.create(
            user=recipient,
             recipient=request.user,  # optional to track origin
            amount=amount,
            transaction_type='credit',
            description=f"Transfer from {request.user.username}",
            status='pending',
        )

        messages.success(request, "Transfer successful.")
        return redirect('dashboard')

    return render(request, 'transfer.html', {'users': users})



@login_required
def pay_bill(request):
    if request.method == 'POST':
        form = PayBillForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            amount = form.cleaned_data['amount']

            if profile.account_balance >= amount:
                profile.account_balance -= amount
                profile.save()

                Transaction.objects.create(
                    user=request.user,
                    amount=amount,
                    transaction_type="debit",
                    description="Direct Deposit - External Bank Transfer",
                    recipient_account_number=form.cleaned_data['account_number'],
                    recipient_routing_number=form.cleaned_data['routing_number'],
                    recipient_bank_name=form.cleaned_data['bank_name'],
                    status="pending"
                )

                print("✅ Payment successful, redirecting...")
                return redirect('dashboard')  # ✅ must match url name
            else:
                form.add_error(None, "Insufficient funds.")
    else:
        form = PayBillForm()

    return render(request, 'pay_bill.html', {'form': form})




@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transactions.html', {'transactions': transactions})

def mobiledepo(request):
    return render (request, "mobiledepo.html")



# @login_required
         # # @require_POST
         # def mark_seen(request):
         #     request.user.notifications.filter(seen=False).update(seen=True)
         #     return JsonResponse({"ok": True})