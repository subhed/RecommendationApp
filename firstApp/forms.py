
from django import forms
from .models import firstModel
from .models import userModel
from .models import postModel
from .models import categoryModel



class firstForm(forms.ModelForm):

    class Meta:
        model = firstModel
        widgets = {
            'sender': forms.TextInput(attrs={'class': 'form-control'}),
            'receiver': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = "__all__"


class userForm(forms.ModelForm):

    class Meta:
        model = userModel
        widgets = {
            'f_name': forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder': 'First Name'}),
            'l_name': forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Re-enter Password'}),
        }
        fields = "__all__"

entries = categoryModel.objects.all()

class postForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=entries,  initial=0)

    class Meta:
        model = postModel
        widgets = {
            'post_message': forms.Textarea(attrs={'class': 'form-control m-2', 'placeholder': 'Ask for recommendation.', 'style': 'height:5em; border:1px solid #fff;'}),
            'user_name': forms.TextInput(attrs={'class': 'form-control m-2', 'style': 'display:none; border:1px solid #fff;', 'placeholder': 'None'}),
            'user': forms.TextInput(attrs={'class': 'form-control m-2', 'style': 'display:none; border:1px solid #fff;', 'placeholder': 'None'}),
            'location': forms.TextInput(attrs={'class': 'form-control col-4 m-2', 'placeholder': 'Enter Location', 'style': 'display:inline;  border:1px solid #fff;','required': 'False'}),
        }
        
        fields = "__all__"
                

