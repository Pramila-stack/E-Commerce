from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email","password1",'password2']

class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        max_length=200,
        label="Full Name",
        widget=forms.TextInput(attrs={'placeholder':'Full Name','class':'form-control'})
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder':'Email','class':'form-control'})
    )

    address = forms.CharField(
        max_length=200,
        label='Address',
        widget=forms.Textarea(attrs={'placeholder':'Address','class':'form-control'})
    )

    city = forms.CharField(
        max_length=50,
        label='City',
        widget=forms.TextInput(attrs={'placeholder':'City','class':'form-control'})
    )

    zip_code = forms.CharField(
        max_length=50,
        label="ZIP CODE",
        widget=forms.TextInput(attrs={'placeholder':'ZipCode','class':'form-control'})
    )

    payment_method = forms.ChoiceField(
        label="Payment Method",
        choices=[("cod","Cash On Delivery"),("card","CARD Payment")],
        widget=forms.Select(attrs={'class':'form-select'})
    )

