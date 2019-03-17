from django import forms
from elibrary.models import Ebook
from django.contrib.auth.models import User


class UploadFileForm(forms.ModelForm):
	# title = forms.CharField(max_length=200)
	file = forms.FileField()
	# uploader = User

	class Meta:
		model = Ebook
		fields = ('file',)
