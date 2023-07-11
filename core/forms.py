from django import forms

from core.models import *
from generate_number import *

DATE_CHOICES = (
    ('Month', "Month"),
    ('Year', "Year")
)


class GenerateForm(forms.Form):
    series = forms.CharField(max_length=3, required=True, widget=forms.TextInput(attrs={'class': 'mb-3'}))
    count = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'mb-3'}))
    period = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'mb-3'}))
    date = forms.ChoiceField(required=True, choices=DATE_CHOICES, widget=forms.RadioSelect())

    def clean_date(self):
        series = self.cleaned_data['series']
        date = self.cleaned_data['date']
        count = self.cleaned_data['count']
        period = self.cleaned_data['period']
        if len(str(series)) != 3:
            self.add_error('series', 'The number of beech trees should be three')
        if 0 > count or count > 20:
            self.add_error('count', 'The number does not satisfy the condition')
        if period > 11:
            self.add_error('period', 'The number does not satisfy the condition')
        elif len(str(series)) == 3 and 0 < count and count < 20 and period < 11:
            generate_card(count, series, date, period)


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = '__all__'
        widgets = {
            'series': forms.widgets.TextInput(attrs={'class': 'mb-3'}),
            'number': forms.widgets.NumberInput(attrs={'class': 'mb-3'}),
            'release_date': forms.widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'mb-3'}),
            'end_date': forms.widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'mb-3'}),
            'cvv': forms.widgets.NumberInput(attrs={'class': 'mb-3'}),
            'funds': forms.widgets.NumberInput(attrs={'class': 'mb-3'}),
            'status': forms.widgets.Select(attrs={'class': 'mb-3'})
        }

    def clean_number(self):
        number = self.cleaned_data['number']
        series = self.cleaned_data['series']
        if len(str(number)) != 16:
            raise forms.ValidationError('The number of digits must be sixteen')
        if Card.objects.filter(number=number).exists() and Card.objects.filter(series=series).exists():
            raise forms.ValidationError('Such a series of cards and numbers already exists')
        else:
            return number

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if len(str(cvv)) != 3:
            raise forms.ValidationError('The number of digits must be three')
        return cvv


class EditCardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['series', 'release_date', 'end_date', 'cvv', 'funds']
        widgets = {
            'series': forms.widgets.TextInput(attrs={'class': 'mb-3'}),
            'release_date': forms.widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'mb-3'}),
            'end_date': forms.widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'mb-3'}),
            'cvv': forms.widgets.NumberInput(attrs={'class': 'mb-3'}),
            'funds': forms.widgets.NumberInput(attrs={'class': 'mb-3'}),
        }

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if len(str(cvv)) != 3:
            raise forms.ValidationError('The number of digits must be three')
        return cvv


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'
        widgets = {
            'title': forms.widgets.TextInput(attrs={'class': 'mb-3'}),
            'price': forms.widgets.NumberInput(attrs={'class': 'mb-3'}),
            'address': forms.widgets.TextInput(attrs={'class': 'mb-3'}),
            'card': forms.widgets.Select(attrs={'class': 'mb-3'})
        }

    def clean_card(self):
        price = self.cleaned_data['price']
        card = self.cleaned_data['card']
        if int(card.funds) + int(price) < 0:
            self.add_error('price', 'Your account does not have enough funds')
        if price == 0:
            self.add_error('price', 'Unable to complete the purchase, please enter another number')
        elif int(card.funds) + int(price) >= 0:
            card.funds = int(card.funds) + int(price)
            card.save()
        return card
