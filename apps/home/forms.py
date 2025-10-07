from datetime import timezone

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from apps.home.models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('user', 'guests', 'room', 'check_in', 'check_out', 'phone')
        widgets = {
            'check_in': forms.DateField(),
            'check_out': forms.DateField(),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
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
    def clean(self):
        check_in = self.cleaned_data.get('check_in')
        check_out = self.cleaned_data.get('check_out')
        room = self.cleaned_data.get('room')

        if check_in >= check_out:
            raise ValidationError("The check-out date must be later than the check-in date.")

        if check_in < timezone.now():
            raise ValidationError("The check-in date must be later than the current date.")

        if not room.is_available(check_in, check_out):
            raise ValidationError("The room must be available.")
