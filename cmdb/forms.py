from django import forms
from .models import Operator, GameProject, GameVersion, Host

class OperatorForm(forms.ModelForm):
    class Meta:
        model = Operator
        exclude = ["id",]
        error_css_class = 'error'
        required_css_class = 'required'
        

class GameProjectForm(forms.ModelForm):
    class Meta:
        model = GameProject
        exclude = ["id",]
        error_css_class = 'error'
        required_css_class = 'required'

        
class GameVersionForm(forms.ModelForm):
    class Meta:
        model = GameVersion
        exclude = ["id",]
        error_css_class = 'error'
        required_css_class = 'required'

        
class AssetForm(forms.ModelForm):
    class Meta:
        model = Host
        exclude = ["id",]
        error_css_class = 'error'
        required_css_class = 'required' 

        