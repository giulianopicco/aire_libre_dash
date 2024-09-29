from django.shortcuts import render

import plotly.express as px
import pandas as pd

from aire_libre.forms import MesurementsForm
from . import utils

# Create your views here.


def index(request):

    period = int(request.GET.get('period', 1))
    source = request.GET.get('source', '6909e3')

    data = utils.fetch_data(source, period)

    df = pd.DataFrame(data)
    print(df.head())

    # Convert 'recorded' to datetime format
    df['recorded'] = pd.to_datetime(df['recorded'])

    # Create 'date' and 'hour' columns
    df['date'] = df['recorded'].dt.date
    df['hour'] = df['recorded'].dt.hour

    # Create pivot table
    pivot_df = df.pivot_table(
        values='pm2dot5', index='date', columns='hour')

    print(pivot_df)

    fig = px.imshow(pivot_df, color_continuous_scale=[
        "green", 'yellow', 'red', "brown"], title="PM 2.5 concentration")
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1,
            showgrid=False
        ),
        yaxis={
            'tickformat': '%Y-%m-%d',
            'tickmode': 'linear',
            'showgrid': False
        },
        height=800,
    )

    form = MesurementsForm()

    context = {
        'fig': fig.to_html(),
        'form': form
    }

    if request.htmx:
        return render(request, 'aire_libre/partials/chart.html', context)

    return render(request, 'aire_libre/index.html', context)
