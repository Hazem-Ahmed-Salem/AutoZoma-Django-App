from django import forms
from .models import Listing
from users.widgets import CustomPictureWidget

class ListingForm(forms.ModelForm):
    image = forms.ImageField(widget=CustomPictureWidget)
    class Meta:
        model=Listing
        fields=('brand','model','vin','mileage',
                'color','engine','transmission',
                'image','description'
        )

class ListingForm_without_widgets(forms.ModelForm):
    
    class Meta:
        model=Listing
        fields=('brand','model','vin','mileage',
                'color','engine','transmission',
                'image','description'
        )