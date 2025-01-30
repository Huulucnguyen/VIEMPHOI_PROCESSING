from django import forms
from .models import PatientXray

class PatientXrayForm(forms.ModelForm):
    class Meta:
        model = PatientXray
        fields = ['name','Xray_image']
