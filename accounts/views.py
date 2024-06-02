from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from accounts.models import Address, User
from django.contrib import messages
from base.utils import send_password_reset_email
from django.contrib.auth.decorators import login_required
import uuid

@login_required(login_url='login')
def user_profile(request, email):
    if request.user.email==email:
        if request.method == "POST":
            user = User.objects.get(email=email)
            if "profile_picture" in request.FILES:
                user.user_image.delete()
                user.user_image = request.FILES.get('profile_picture')
                user.save()
                messages.success(request, 'Profile updated successfully')
                return HttpResponseRedirect(request.path_info)
            else:
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                phone_number = request.POST.get('phone_number')
                user.first_name = first_name
                user.last_name = last_name
                user.phone_number = phone_number
                user.save()
                messages.success(request, 'Profile updated successfully')
                return HttpResponseRedirect(request.path_info)
        
        return render(request, 'accounts/profile.html')
    else:
        messages.warning(request, 'You are not authorized to access this page')
        return HttpResponseRedirect(request.path_info)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email)

        if not user.exists():
            messages.warning(request, 'Account not found')
            return HttpResponseRedirect(request.path_info)
        
        user = authenticate(email=email, password=password)
        if user is not None:
            if not user.is_email_verified:
                messages.warning(request, 'Please verify your email')
                return HttpResponseRedirect(request.path_info)
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, 'Invalid Credentials')

    return render(request, 'accounts/login.html')

def registerUser(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not first_name or not last_name or not email or not password:
            messages.warning(request, 'All fields are required')

        elif User.objects.filter(email=email).exists():
            messages.warning(request, 'User Already Exists!!')

        else:
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()
            messages.success(request, 'User Created Successfully, Mail has been sent!!')

    return render(request, 'accounts/register.html')

def logoutUser(request):
    logout(request)
    return redirect('/')

def activateUser(request, email_token):
    try:
        user = User.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        login(request, user)
        messages.success(request, 'Email Verified Successfully!!')
    except User.DoesNotExist:
        messages.warning(request, 'Invalid Token!!')
    return redirect('/')

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, 'Account not found')
            return HttpResponseRedirect(request.path_info)
        
        reset_password_token = str(uuid.uuid4())
        print(reset_password_token)
        user.reset_password_token = reset_password_token
        send_password_reset_email(email, reset_password_token)
        user.save()
        messages.success(request, 'Password Reset Email Sent!!')
    
    return render(request, 'accounts/reset_password.html')

def reset_password_confirm(request, reset_password_token):
    try:
        user = User.objects.get(reset_password_token=reset_password_token)
    except User.DoesNotExist:
        messages.warning(request, 'Invalid Token!!')
        return HttpResponseRedirect(request.path_info)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not new_password or not confirm_password:
            messages.warning(request, 'All fields are required')
        elif new_password != confirm_password:
            messages.warning(request, 'New Passwords do not match')
        else:
            user.set_password(new_password)
            user.reset_password_token = None  # Remove reset token after password change
            user.save()
            logout(request)
            messages.success(request, 'Password Reset Successfully!!')
            return redirect('login')  # Redirect to a success page after password reset

    return render(request, 'accounts/reset_password_confirm.html')

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not old_password or not new_password or not confirm_password:
            messages.warning(request, 'All fields are required')
            return render(request, 'accounts/change_password.html')

        user = request.user
        if not user.check_password(old_password):
            messages.warning(request, 'Old Password is incorrect')
            return render(request, 'accounts/change_password.html')

        if new_password!= confirm_password:
            messages.warning(request, 'New Passwords do not match')
            return render(request, 'accounts/change_password.html')

        user.set_password(new_password)
        user.save()
        logout(request)
        messages.success(request, 'Password Changed Successfully!!, Login Again')
        return redirect('login')

    return render(request, 'accounts/change_password.html')

@login_required(login_url='login')
def address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')

        Address.objects.create(user=request.user, name=name, phone_number=phone_number, address=address, pincode=pincode)
        messages.success(request, 'Address Added Successfully!!')

    return render(request, 'accounts/address.html')