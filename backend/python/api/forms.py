from django import forms

class GreetForm(forms.Form):
    name=forms.CharField()
    age=forms.IntegerField(min_value=0)
