from django import forms
from .models import ChamaGroup

class ChamaGroupForm(forms.ModelForm):
    class Meta:
        model = ChamaGroup
        fields = ['name', 'contribution_amount', 'savings_rate', 'frequency']