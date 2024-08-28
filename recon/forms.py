from django import forms

class ReconForm(forms.Form):
    bank_file = forms.FileField(label='Bank File')
    vendor_file = forms.FileField(label='Vendor File')
