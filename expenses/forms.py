
from django import forms
from .models import Document,MyModel,DocumentUpload


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['author', 'title', 'file']
        widgets = {
            "author": forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'name': 'author', },),
            "title": forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'name': 'title', },),

        }

class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['name', 'description', 'file']

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = DocumentUpload
        fields = ['name', 'description', 'file']
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'name': 'name', },),
            "description": forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'name': 'description', },),

        }
