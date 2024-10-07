import json
from django import forms
import requests

periods = [(1, "Día"), (7, "Semana"), (30, "Mes")]


class MesurementsForm(forms.Form):
    period = forms.ChoiceField(choices=periods, initial=7, label='Periodo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        response = requests.get('https://rald-dev.greenbeep.com/api/v1/aqi')
        try:
            data = response.json()
        except json.decoder.JSONDecodeError as e:
            print(e)
            data = []
        choices = [(choice['source'], choice['description'])
                   for choice in data]
        choices.insert(0, ('', '----'))
        self.fields['source'] = forms.ChoiceField(
            choices=choices, label='Fuente (sensor)')
