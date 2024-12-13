from django import forms
from .models import *


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','status']
    
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})
            
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title','description','price','stock','image','color','size','status']
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})

