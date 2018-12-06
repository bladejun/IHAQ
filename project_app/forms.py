from django import forms
from .models import ClassNode

class ClassNodeForm(forms.ModelForm):
	class Meta:
		model = ClassNode
		fields = {'class_name', 'class_id', 'founder_id', 'image', 'founder_name'}