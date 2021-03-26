from django import forms
from .models import Profile, Review
from django.contrib.auth.models import User


class FindMovieForm(forms.Form):
    find = forms.CharField(label='Find', required=False)


class FindReviewerForm(forms.Form):
    find = forms.CharField(label='Find', required=False)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['commentTitle', 'comment', ]


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['userPic']
        labels = {
            'userPic': 'プロフィール写真',
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['userComment']
        labels = {
            'userComment': 'プロフィール',
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        labels = {
            'username': 'ニックネーム',
        }
