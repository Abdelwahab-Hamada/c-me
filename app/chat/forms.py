from django.forms import ModelForm, CharField
from .models import MessageAttachment


class UploadForm(ModelForm):
    chat_id = CharField(max_length=255, required=True)
    text = CharField(max_length=255, required=True)
    class Meta:
        model = MessageAttachment
        fields = ['file']