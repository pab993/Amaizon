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
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(min_length=5, max_length=30)
    email = forms.EmailField()

    def clean(self):
        cd = self.cleaned_data
        try:
            user = User.objects.get(username=cd.get('username'))
        except User.DoesNotExist:
            user = None
        if cd.get('password') != cd.get('password_confirm'):
            self.add_error('password_confirm', "Passwords do not match")
        if user is not None:
            self.add_error('username', 'Username already in use')
        return cd

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']