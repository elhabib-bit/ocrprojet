from django import forms
class imgform(forms.Form):
    image = forms.FileField(label="image",required=True)