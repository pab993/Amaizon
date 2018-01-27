from django.contrib.auth.models import User
from django import forms
from .models import Product, Assessment, UserProfile, ControlPanel


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


class ProfileForm1(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm2(forms.ModelForm):
    picture = forms.FileField(required=False, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ['picture']


CHOICES = (('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1'))


class AssessmentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea)
    score = forms.ChoiceField(choices=CHOICES, required=True)
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput(), required=False)

    def clean(self):
        cd = self.cleaned_data
        if cd.get('comment') is None:
            self.add_error('comment', "Cannot be empty")
        return cd

    class Meta:
        model = Assessment
        fields = ['comment', 'score', 'product']


class ControlPanelForm(forms.ModelForm):
    threshold = forms.IntegerField(required=True, min_value=1)

    def clean(self):
        cp = self.cleaned_data
        if cp.get('threshold') is None:
            self.add_error('threshold', "Cannot be empty")
        return cp

    class Meta:
        model = ControlPanel
        fields = ['threshold']
