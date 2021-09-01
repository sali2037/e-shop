from django import forms
from accounts.models import BilingAdress
class BilingAdressForm(forms.ModelForm):
    class Meta:
        model=BilingAdress
        fields=['country','state','street','hause_number','postalconde',]
    def __init__(self,*args,**kwargs):
        super(BilingAdressForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
        self.fields['country'].widget.attrs['placeholder']= 'In Welchem Land leben Sie?'
        self.fields['state'].widget.attrs['placeholder']= 'In Welchem Bundes land leben Sie?'
        self.fields['street'].widget.attrs['placeholder']= 'In Welcher Strsse leben Sie?'
        self.fields['hause_number'].widget.attrs['placeholder']= 'Haus Nummer'
        self.fields['hause_number'].widget.attrs['label']= 'Haus Nummer'
        self.fields['postalconde'].widget.attrs['placeholder']= 'Ihre postal code'
