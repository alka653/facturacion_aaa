from django.forms import *
from django import forms
from .models import *

class ProductForm(forms.ModelForm):
	class Meta:
		model = Producto
		fields = '__all__'
		widgets = {
			'name': TextInput(attrs = {'class': 'form-control', 'maxlength': '50', 'required': True}),
			'price': TextInput(attrs = {'class': 'form-control number-val', 'required': True})
		}
		labels = {
			'name': 'Nombre del producto',
			'price': 'Precio del producto'
		}