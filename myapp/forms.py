from django import forms
from .models import Profile,Choices
from django.core.validators import MaxValueValidator, MinValueValidator


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = ('user',)
		# fields = '__all__'

class buyForm(forms.Form):
	name = forms.CharField( required=True,label="Name",
	widget=forms.TextInput(attrs={'placeholder':"the card's owner fullname",'class':'form-control'}))

	credit = forms.CharField(required=True,label="Credit Card No.",
			widget=forms.TextInput(attrs={'placeholder':"Credit No.",'class':'form-control'}))

	shares = forms.IntegerField(required="True", label="Shares' Amount",
			widget=forms.NumberInput(attrs={'placeholder':"to buy",'class':'form-control'}))

	month = forms.IntegerField(required="True", label="Month",
			widget=forms.NumberInput(attrs={'class':'form-control'}))

	year = forms.IntegerField(required="True", label="Year",
			widget=forms.NumberInput(attrs={'class':'form-control'}))

	# # mChoices = [('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'),('6', '6'),('7', '7'),
	# # ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')]
	# month = forms.ChoiceField(widget=forms.RadioSelect(choices=Choices.mChoices,attrs={'class':'form-control'}), required=True,label="Month")
	# # yChoices = [('1', '20'), ('2', '22'), ('3', '23'), ('4', '24'), ('5', '25')]
	# year = forms.ChoiceField(widget=forms.RadioSelect(choices=Choices.yChoices,attrs={'class':'form-control'}), required=True,label="Year")
	cvv = forms.IntegerField(required="True", label="CVV",
							 widget=forms.TextInput(attrs={'class':'form-control'}))


