from django import  forms

class ZhengHouForm(forms.Form):
  zh_name = forms.CharField(label='Name', max_length=100)
  zh_message = forms.CharField(widget=forms.Textarea)
  zh_result = forms.CharField(widget=forms.Textarea,required=False)
  zh_is = forms.BooleanField(required=False)
