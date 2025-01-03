# from django import forms
# from .models import Injury
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit

# class InjuryForm(forms.ModelForm):
#     class Meta:
#         model = Injury
#         fields = ['issue', 'area', 'side', 'start_datetime', 'severity', 'description']
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('submit', 'Save Injury'))


from django import forms

# from health.models import Injury

# class InjuryForm(forms.ModelForm):
#     class Meta:
#         model = Injury
#         fields = ['issue', 'area', 'side', 'start_datetime', 'severity', 'description']

class InjurySummaryFilterForm(forms.Form):
    date_from = forms.DateField(required=False, label='Date From', widget=forms.DateInput(attrs={'type': 'date'}))
    