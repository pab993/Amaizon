from django.contrib.auth.models import User
from django import forms
from .models import Product, Assessment


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'picture', 'pub_date']


class AssessmentForm(forms.ModelForm):

    class Meta:
        model = Assessment
        fields = ['comment', 'score']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
