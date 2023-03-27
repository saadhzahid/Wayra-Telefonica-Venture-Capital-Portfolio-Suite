from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from portfolio.forms import ChangePasswordForm, ContactDetailsForm, ProfilePictureForm

"""
View and Update user settings
"""


@login_required
def account_settings(request):
    current_user = request.user
    change_password_form = ChangePasswordForm(user=current_user)
    contact_details_form = ContactDetailsForm(user=current_user, instance=request.user)
    profile_picture_form = ProfilePictureForm(instance=request.user)
    context = {
        "user": current_user,
        "change_password_form": change_password_form,
        "contact_details_form": contact_details_form,
        "profile_picture_form": profile_picture_form,
    }
    return render(request, 'settings/account_settings.html', context)


@login_required
def upload_profile_picture(request):
    if request.method == "POST":
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Profile Pictuer Updated Successfully!")
            return redirect('account_settings')
        else:
            messages.add_message(request, messages.ERROR, "Unable to update your profile picture!")
            current_user = request.user
            change_password_form = ChangePasswordForm(user=current_user)
            contact_details_form = ContactDetailsForm(user=current_user, instance=request.user)
            context = {
                "user": current_user,
                "change_password_form": change_password_form,
                "contact_details_form": contact_details_form,
                "profile_picture_form": form,
            }
            return render(request, 'settings/account_settings.html', context)
    else:
        return HttpResponse("404, Unable to make this call")


@login_required
def remove_profile_picture(request):
    if request.user.profile_picture:
        request.user.profile_picture.delete()
        messages.add_message(request, messages.SUCCESS, "Successfully removed your profile picture!")
    else:
        messages.add_message(request, messages.ERROR, "You do not have a profile picture!")
    return redirect("account_settings")


@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            # Change the user's password
            form.save()
            update_session_auth_hash(request, form.user)

            messages.add_message(request, messages.SUCCESS, "Password Updated Successfully!")
            return redirect('account_settings')
        else:
            messages.add_message(request, messages.ERROR, "Unable to change your password!")
            current_user = request.user
            contact_details_form = ContactDetailsForm(user=current_user, instance=request.user)
            profile_picture_form = ProfilePictureForm(instance=request.user)
            context = {
                "user": current_user,
                "change_password_form": form,
                "contact_details_form": contact_details_form,
                "profile_picture_form": profile_picture_form,
            }
            return render(request, 'settings/account_settings.html', context)
    else:
        return HttpResponse("404, Unable to make this call")


@login_required
def contact_details(request):
    if request.method == "POST":
        form = ContactDetailsForm(data=request.POST, user=request.user, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Details Updated Successfully!")
            return redirect('account_settings')
        else:
            messages.add_message(request, messages.ERROR, "Unable to change your details!")
            current_user = request.user
            profile_picture_form = ProfilePictureForm(instance=request.user)
            change_password_form = ChangePasswordForm(user=current_user)
            context = {
                "user": current_user,
                "change_password_form": change_password_form,
                "profile_picture_form": profile_picture_form,
                "contact_details_form": form,
            }
            return render(request, 'settings/account_settings.html', context)
    else:
        return HttpResponse("404, Unable to make this call")


@login_required
def deactivate_account(request):
    user = request.user
    logout(request)
    user.delete()
    messages.add_message(request, messages.SUCCESS, "Account successfully deactivated!")
    return redirect('login')
