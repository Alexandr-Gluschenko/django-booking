from django import forms
from django.core.validators import RegexValidator

from apps.home.models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('guest_count', 'room', 'rooms_count', 'start_date', 'end_date', 'phone')
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guest_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'rooms_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
        }

    phone = forms.CharField(
        max_length=15,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{8,15}$',
                message="Phone number must be entered in digits only (8-15 digits)."
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your phone number',
            'class': 'form-control'
        })
    )
