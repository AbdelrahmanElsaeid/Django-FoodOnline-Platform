from django import forms
from .models import Category, FoodItem
from accounts.validators import allow_only_images_validator
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','description']




class FooditemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    class Meta:
        model = FoodItem
        fields = ['food_title','category','description','price','image','is_available']        