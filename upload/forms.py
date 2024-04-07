from django import forms
from .models import PDFDocument

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['title', 'file']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
