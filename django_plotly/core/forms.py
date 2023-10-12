from django import forms


class DateForm(forms.Form):
    start = forms.IntegerField(min_value=2015, max_value=2022)
    end = forms.IntegerField(min_value=2015, max_value=2022)