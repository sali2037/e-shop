from django import forms
from store.models import ReviewRating

class ReviewForm(forms.ModelForm):
    class Meta:
        model=ReviewRating
        fields=['subject', 'review','rating']
    def __init__(self,*args,**kwargs):
        super(ReviewForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
