from django import forms

class DateForm(forms.Form):
	init_date = forms.DateField()
	fin_Date = forms.DateField()