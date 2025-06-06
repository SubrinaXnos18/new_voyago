from django import forms
from .models import Package, Contact

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'contact_number', 'comments']