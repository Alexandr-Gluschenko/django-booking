from datetime import timezone

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking


class BookingForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=15,
        required=True,
        validators=[
            RegexValidator(
                r'^\+380\d{9}$',
                "Phone must be in format +380XXXXXXXXX"
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+380XXXXXXXXX'
        })
    )

    class Meta:
        model = Booking
        fields = ('room', 'guests', 'check_in', 'check_out', 'phone')
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            if check_in >= check_out:
                raise ValidationError("The check-out date must be later than the check-in date.")

            if check_in < timezone.now():
                raise ValidationError("The check-in date must be later than the current date.")
        return cleaned_data


class BookSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search",
                "class": "form-control"
            }
        )
    )
