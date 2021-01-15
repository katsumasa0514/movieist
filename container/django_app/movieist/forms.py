from django import forms
from .models import Profile, Review


class FindForm(forms.Form):
    find = forms.CharField(label='Find', required=False)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['userPic', ]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['commentTitle', 'comment', ]
