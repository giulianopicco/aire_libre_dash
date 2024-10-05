from django import forms
import requests

periods = [(1, "Day"), (7, "Week"), (30, "Month")]


class MesurementsForm(forms.Form):
    period = forms.ChoiceField(choices=periods, initial=7)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        response = requests.get('https://rald-dev.greenbeep.com/api/v1/aqi')
        data = response.json()
        choices = [(choice['source'], choice['description'])
                   for choice in data]
        choices.insert(0, ('', '----'))
        self.fields['source'] = forms.ChoiceField(
            choices=choices)
