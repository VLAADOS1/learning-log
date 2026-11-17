from django import forms

from .models import Entry, Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["text"]


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["text"]
        widgets = {"text": forms.Textarea(attrs={"rows": 8})}
