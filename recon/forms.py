from django import forms
from recon.models import LoanApplication


class ReconForm(forms.Form):
    bank_file = forms.FileField(label='Bank File')
    vendor_file = forms.FileField(label='Vendor File')

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = [
            'name', 'email', 'phone', 'address', 'loan_type', 'govt_id_type',
            'govt_id_number', 'govt_id_upload', 'photo_capture',
            'home_coordinates', 'collateral_type', 'collateral_coordinates',
            'collateral_details'
        ]
        widgets = {
            'loan_type': forms.RadioSelect(),
            'collateral_type': forms.TextInput(attrs={'placeholder': 'E.g., Land, Vehicle'}),
        }