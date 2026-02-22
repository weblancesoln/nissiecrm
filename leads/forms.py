from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Lead


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class StyledUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class LeadForm(forms.ModelForm):
    """Form for creating and editing leads."""

    class Meta:
        model = Lead
        fields = [
            'first_name', 'last_name', 'phone_number', 'email',
            'point_of_contact', 'prospect_response', 'remarks',
            'status', 'color_code', 'source', 'assigned_to',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Last name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '+234 800 000 0000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'email@example.com'
            }),
            'point_of_contact': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. Website, John Doe referral'
            }),
            'prospect_response': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3, 'placeholder': 'Their response or feedback'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3, 'placeholder': 'Internal notes'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'color_code': forms.Select(attrs={'class': 'form-select'}),
            'source': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. Website, Social Media'
            }),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth.models import User
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('username')
        self.fields['assigned_to'].required = False
        self.fields['assigned_to'].empty_label = '— Unassigned —'


class LeadUploadForm(forms.Form):
    """Form for bulk uploading leads via CSV or Excel."""

    file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv,.xlsx,.xls'
        })
    )
