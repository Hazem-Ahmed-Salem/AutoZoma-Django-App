from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate , login ,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from main.models import Listing ,LikedListing
from .forms import ProfileForm , UserForm , LocationForm,RegisterForm 
from django.http import JsonResponse
from .models import Profile

def login_view(request):
    
    if request.method =='POST':
        login_form=AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username=login_form.cleaned_data.get("username")
            password=login_form.cleaned_data.get("password")
            user=authenticate(username=username, password=password)
            if user:
                login(request , user)
                messages.success(request, f'you are now logged in as {username}')
                return redirect('home')
            
        else:
            messages.error(request, f'An Error occured while trying to log you in')
    else:
        if request.user.is_authenticated:
            return redirect('home')
        login_form=AuthenticationForm()    
    return render(request , 'views/login.html' , {'login_form':login_form})

class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        
        return render(request, 'views/register.html', {'register_form':register_form})
    
    def post(self,request):
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid() :
            user = register_form.save()
            user.refresh_from_db()
            if user:
                login(request,user)
                messages.success(request,f'User {user.username} registered successfully.')
                return redirect('home')
        else:
            messages.error(request, f'An error occured trying to register')
            return render(request, 'views/register.html', {'register_form':register_form})


def logout_view(request):
    logout(request)
    return redirect('main')


@method_decorator(login_required ,name='dispatch')
class ProfileView(View):

    def post(self , request):
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        location_form=LocationForm(request.POST,instance=request.user.profile.location)
        if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
            user_form.save()
            profile_form.save()
            location_form.save()
            messages.success(request ,'Profile was updated successfully')
        else:
            messages.error(request,'An Error has occured while updating your Profile')
        return redirect('profile')

    def get(self,request):
        user_liked_listings=LikedListing.objects.filter(profile=request.user.profile)
        user_listings = Listing.objects.filter(seller=request.user.profile)
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        location_form=LocationForm(instance=request.user.profile.location)
        context = {
        'user_form':user_form , 'profile_form':profile_form ,
        'location_form':location_form, 'user_listings':user_listings,
        'user_liked_listings':user_liked_listings }
        return render(request, 'views/profile.html', context)

@login_required
def profile_others_view(request, id):
    if request.method == 'GET':
        try:
            user = get_object_or_404(Profile,id=id)
            listing =  Listing.objects.filter(seller=user)
            liked_listings=LikedListing.objects.filter(profile=user)
        except Exception as e:
            messages.error(request,f"Something went wrong while getting this user id({id})")
            print(f'Error:',e)
            return redirect('home')

        context={
            'profile_user':user,
            'user_listings':listing,
            'user_liked_listings':liked_listings
        }
        return render(request,'views/profile_other.html',context)
    else:
        return JsonResponse({
            'error':'Wrong HTTP Method',
            'message':'try using another HTTP method'
        })

