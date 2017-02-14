from django import forms
from .models import Comment
class EmailPostForm(forms.Form):
    name = forms.CharField(label="نام",max_length=25)
    email = forms.EmailField(label="ایمیل شما")
    to = forms.EmailField()
    comments = forms.CharField(label="دیدگاه",required=False, widget = forms.Textarea)
    #for places that we dont interact with database and models we use forms.Form

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')
