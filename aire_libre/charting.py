import plotly.graph_objects as go

from aire_libre import utils


def get_line_chart(data, title):
    layout = dict(
        hoversubplots="axis",
        title=title,
        hovermode="x",
        grid=dict(rows=3, columns=1),
    )

    data = [
        go.Scatter(x=data["recorded"], y=data["pm2dot5"],
                   xaxis="x", yaxis="y", name="PM2.5", fill='tozeroy'),
        go.Scatter(x=data["recorded"], y=data["pm10"],
                   xaxis="x", yaxis="y2", name="PM10", fill='tozeroy'),
        go.Scatter(x=data["recorded"], y=data["pm1dot0"],
                   xaxis="x", yaxis="y3", name="PM0.1", fill='tozeroy'),
    ]

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(template='plotly_dark')

    return fig


def get_heatmap_chart(data, period, title):
    pivot_df = data.pivot_table(
        values='pm2dot5', index='date', columns='hour')

    pivot_df = pivot_df.map(lambda x: utils.get_quality(x))

    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        z=pivot_df,
        x=pivot_df.columns,
        y=pivot_df.index,
        xgap=5,
        ygap=5,
        colorscale=[
            [0, "yellowgreen"],
            [.125, "yellowgreen"],
            [.125, "gold"],
            [.25, "gold"],
            [.25, "darkorange"],
            [.375, "darkorange"],
            [.375, "tomato"],
            [.5, "tomato"],
            [.5, "darkorchid"],
            [.833, "darkorchid"],
            [.833, "maroon"],
            [1, "maroon"],
        ],
        zmin=0,
        zmax=400,
        hovertemplate='<b>Fecha: %{y}</b><br><b>Hora: %{x}</b><br><b>Aqi: %{z}</b>',
        name="",
        colorbar=dict(thickness=25,
                      title=dict(
                          text="Escala AQI",
                      ),
                      tickvals=[25, 75, 125, 175, 250, 350],
                      ticktext=['Bueno', 'Moderado', 'Peligroso para grupos sensibles',
                                'Insalubre', 'Muy insalubre', 'Peligroso'],)
    ))

    hours = [f'{i:02d}' for i in range(24)]
    fig.update_xaxes(
        ticktext=hours,
        tickvals=list(range(24)),
        showgrid=False,
        zeroline=False
    )

    fig.update_yaxes(
        tickformat='%Y-%m-%d',
        tickmode='linear',
        showgrid=False,
        zeroline=False,
        autorange="reversed"
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        height=300 + 40 * period,
        title=title,
        xaxis_title="Hora",
        yaxis_title="Fecha",
        template="plotly_dark"
    )

    return fig


def get_stats_data(source, period):
    stats = utils.fetch_stats(source, period)
    pm_values = {
        'pm2dot5': stats[0]['pm2dot5'],
        'pm10': stats[0]['pm10'],
        'pm1dot0': stats[0]['pm1dot0']
    }

    return pm_values
