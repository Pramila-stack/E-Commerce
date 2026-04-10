from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# 🔐 SIGNUP FORM (Improved)
class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label
            })


# 🛒 CHECKOUT FORM (Improved)
class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        max_length=200,
        label="Full Name",
        widget=forms.TextInput(attrs={
            'placeholder': 'Full Name',
            'class': 'form-control'
        })
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'form-control'
        })
    )

    address = forms.CharField(
        max_length=200,
        label='Address',
        widget=forms.Textarea(attrs={
            'placeholder': 'Address',
            'class': 'form-control',
            'rows': 3
        })
    )

    city = forms.CharField(
        max_length=50,
        label='City',
        widget=forms.TextInput(attrs={
            'placeholder': 'City',
            'class': 'form-control'
        })
    )

    zip_code = forms.CharField(
        max_length=10,
        label="ZIP Code",
        widget=forms.TextInput(attrs={
            'placeholder': 'Zip Code',
            'class': 'form-control'
        })
    )

    payment_method = forms.ChoiceField(
        label="Payment Method",
        choices=[
            ("cod", "Cash On Delivery"),
            ("card", "Card Payment")
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # ✅ CUSTOM VALIDATION
    def clean_zip_code(self):
        zip_code = self.cleaned_data.get("zip_code")

        if not zip_code.isdigit():
            raise forms.ValidationError("ZIP code must contain only numbers.")

        return zip_code

    def clean_full_name(self):
        name = self.cleaned_data.get("full_name")

        if len(name.split()) < 2:
            raise forms.ValidationError("Please enter your full name.")

        return name

