from django.shortcuts import render, redirect ,get_object_or_404
from django.http import HttpResponse ,JsonResponse
from django.contrib.auth.decorators import login_required
from users.forms import LocationForm
from django.core.mail import send_mail
from .models import Listing ,LikedListing
from .forms import ListingForm ,ListingForm_without_widgets
from .filter import ListingFilter
from django.contrib import messages

def  main_view(request):
    return render(request , 'views/main.html')

@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)
    user_liked_listings = LikedListing.objects.filter(profile=request.user.profile).values_list('listing')
    liked_listing_ids = [l[0] for l in user_liked_listings]
    context={
        'listing_filter':listing_filter,
        'liked_listing_ids':liked_listing_ids
    }
    return render(request, 'views/home.html' , context)


@login_required
def list_view(request):
    listing_form = ListingForm_without_widgets()
    location_form = LocationForm()
    context = {
        'listing_form':listing_form ,
        'location_form':location_form,
    }
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST)
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location = location_form.save()
                listing.seller = request.user.profile
                listing.location =  listing_location
                listing.save()
                messages.info(request ,f'{listing.brand} {listing.model} Listing was Posted Successfully  ')
                return redirect('home')
            else:
                raise Exception()
        except Exception as error:
            print(error)
            messages.error(request ,'An error has occured while posting the listing of your car.')
    return render(request,'views/list.html', context)


@login_required
def listing_view(request , id ):
    try:
        listing = Listing.objects.get(id=id)
        context = {'listing':listing}
        if listing is None:
            raise Exception()
        return render(request,'views/listing_page.html', context )
    except Exception as e:
        messages.error(request, f'Invalid UID {id} was provided for listing')
        return redirect('home')
    
@login_required
def edit_view(request , id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None :
            raise Exception()
        if request.method == "POST":
            listing_form = ListingForm(request.POST , request.FILES , instance=listing)
            location_form = LocationForm(request.POST , instance=listing.location)
            if listing_form.is_valid() and location_form.is_valid():
                listing_form.save()
                location_form.save()
                messages.success(request,f'Listing was {listing.brand} updated successfully')
                return redirect('edit', id=id )
            else:
                raise Exception()
        else:
            listing_form = ListingForm(instance=listing)
            location_form = LocationForm(instance=listing.location)
            context = { 'listing_form':listing_form ,
                        'location_form':location_form,
                        'listing':listing
                        }
        return render(request, 'views/edit.html' , context )
    except Exception as e:
        messages.error(request,f'{e} An error occured while trying to edit your listing')
        return redirect('home')

@login_required
def delete_listing(request, id):
    listing = Listing.objects.get(id=id)
    if listing :
        listing.delete()
        messages.success(request,f"The car listing was deleted successfully")
        return redirect('home')
    else:
        messages.error(request,f"Something went Wrong while deleting the listing with id({id})")
        return redirect('home')
    

@login_required
def like_listing_view( request , id ):
    listing = get_object_or_404(Listing , id=id)
    liked_listing , created = LikedListing.objects.get_or_create(
        profile = request.user.profile , listing = listing) 
    if not created:
        liked_listing.delete()
    else: 
        liked_listing.save()

    return JsonResponse({
        'is_liked_by_user' : created,
        })

@login_required
def inquire_listing_by_email(request , id):
    if request.method == "POST":
        listing=get_object_or_404(Listing,id=id)
        try:
            subject = f'{request.user.username} is interested in {listing.brand} {listing.model}'
            messages = f'hi {listing.seller.user.username}, {request.user.username} is interested in your {listing.brand} {listing.model} listing on AutoZoma.'
            send_mail(subject=subject ,message=messages ,from_email="noreply@zoma.com" ,recipient_list=[listing.seller.user.email] , fail_silently=False)
            return JsonResponse({
                "success":True,
            })
        except Exception as e:
            print(e)
            return JsonResponse({
                "success":False,
                "info": f'{e}' ,
            })
    else:
        return HttpResponse("<h1> hii are you ok </h1>")
    