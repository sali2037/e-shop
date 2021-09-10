from django import forms
from order.models import Order
class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['first_name','last_name','phone','email','country','state','street','hause_number','postalconde',]
    def __init__(self,*args,**kwargs):
        super(OrderForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
        self.fields['country'].widget.attrs['placeholder']= 'In Welchem Land leben Sie?'
        self.fields['state'].widget.attrs['placeholder']= 'In Welchem Bundes land leben Sie?'
        self.fields['street'].widget.attrs['placeholder']= 'In Welcher Strsse leben Sie?'
        self.fields['hause_number'].widget.attrs['placeholder']= 'Haus Nummer'
        self.fields['hause_number'].widget.attrs['label']= 'Haus Nummer'
        self.fields['postalconde'].widget.attrs['placeholder']= 'Ihre postal code'
        self.fields['first_name'].widget.attrs['placeholder']='Your name'
        self.fields['last_name'].widget.attrs['placeholder']='Your last name'
        self.fields['phone'].widget.attrs['placeholder']='YOUR PHONE Number'
        self.fields['email'].widget.attrs['placeholder']='Your Email Address'
        self.fields['first_name'].widget.attrs['label']='First name :'
