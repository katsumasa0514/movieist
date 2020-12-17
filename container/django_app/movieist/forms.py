from django import forms


class FindForm(forms.Form):
    find = forms.CharField(label='find')
