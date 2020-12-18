from django import forms
from .models import Search


class FindForm(forms.Form):
    find = forms.CharField(label='Find', required=False)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ('userPic',)
