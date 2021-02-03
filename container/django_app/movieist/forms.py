from django import forms
from .models import Profile, Review, User


class FindForm(forms.Form):
    find = forms.CharField(label='Find', required=False)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['commentTitle', 'comment', ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['userPic', 'userComment', ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', ]
