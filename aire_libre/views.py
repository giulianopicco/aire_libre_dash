from django.shortcuts import render

import pandas as pd

from aire_libre import charting
from aire_libre.forms import MesurementsForm
from . import utils


def index(request):

    period = int(request.GET.get('period', 7))
    source = request.GET.get('source', None)

    form = MesurementsForm()

    if source is None:
        context = {
            'form': form,
        }
        return render(request, 'aire_libre/index.html', context)

    data = utils.fetch_data(source, period)
    df = pd.DataFrame(data)
    df['recorded'] = pd.to_datetime(df['recorded'])
    # Shift 'hour' column by 4 hours because of the offset
    df['recorded'] = df['recorded'] - pd.Timedelta(hours=4)
    df['date'] = df['recorded'].dt.date
    df['hour'] = df['recorded'].dt.hour
    df = df.sort_values(by='recorded', ascending=True)

    fig_heatmap = charting.get_heatmap_chart(df, period,
                                             f"Índice de Calidad del Aire (AQI) por hora en {next((y for x, y in form.fields['source'].choices if x == source), None)} en los últimos {period} días")
    fig_line = charting.get_line_chart(df,
                                       f"Cantidad de PM2.5, PM10 y PM10.1 medidas en {next((y for x, y in form.fields['source'].choices if x == source), None)} en los últimos {period} días")

    pm_values = charting.get_stats_data(source, period)

    context = {
        'fig_heatmap': fig_heatmap.to_html(),
        'fig_line': fig_line.to_html(),
        'stats': pm_values,
        'form': form
    }

    if request.htmx:
        return render(request, 'aire_libre/partials/chart.html', context)

    return render(request, 'aire_libre/index.html', context)
