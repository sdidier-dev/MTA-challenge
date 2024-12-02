from dash import Dash, html, Input, Output, clientside_callback, _dash_renderer
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import components as components

from dash_bootstrap_templates import ThemeChangerAIO

_dash_renderer._set_react_version("18.2.0")

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(
    external_stylesheets=[dbc.themes.SOLAR, dbc_css, dmc.styles.DATES],
)

server = app.server

title_layout = html.Div([

    html.Div("New York City MTA Transportation Daily Ridership (Beginning 2020-03)",
             className='flex-grow-1 text-center fs-3'),

    html.Div([
        dmc.Switch(
            id='color-mode-switch',
            offLabel=DashIconify(icon="radix-icons:moon", width=20),
            onLabel=DashIconify(icon="radix-icons:sun", width=20),
            size="lg", color='var(--bs-primary)',
            styles={"track": {'border': '2px solid var(--bs-primary)'}},
        ),
        ThemeChangerAIO(
            aio_id="theme",
            radio_props=dict(value=dbc.themes.SOLAR),
            button_props=dict(outline=False, color="primary"),
            offcanvas_props={"placement": "end"}
        ),
        html.A(
            DashIconify(icon="mdi:github", width=34),
            href="https://github.com/sdidier-dev/mta-challenge", target="_blank", className='text-body mx-2'
        ),
    ], className='d-inline-flex gap-2'),
], className='d-flex align-items-center bg-gradient border-bottom border-primary border-2 mx-2', style={'height': 60})

main_layout = html.Div([

    components.MTA_key_figures_grid,

    html.Div([
        dbc.Card([
            dbc.CardHeader(components.MTA_aggregate_title_controls,
                           className='d-flex justify-content-center fs-5 text-body text-nowrap'),
            dbc.CardBody(components.MTA_aggregate_bar, className='p-0'),
        ], className='flex-fill', style={'min-width': 700, 'min-height': 500}),

        dbc.Card([
            dbc.CardHeader([
                dmc.Tooltip(
                    dmc.ActionIcon(
                        DashIconify(icon='clarity:info-line', width=25),
                        id="level-info-map-btn",
                        variant="transparent", color='var(--bs-primary)'),
                    multiline=True, withArrow=True, arrowSize=6, w=500, position="bottom",
                    label="Each transportation uses an ARIMA model to make the predictions. "
                          "The hyperparameters of each model have been fine-tuned with optuna optimization "
                          "using cross validation with an expanding window and the "
                          "'mean absolute percentage error' (MAPE) as metric",
                    classNames={
                        'tooltip': 'bg-body text-body border border-primary',
                        'arrow': 'bg-body border-top border-start border-primary'
                    },
                ),
                'Ridership Prediction for the Next 30 Days'
            ], className='d-flex justify-content-center fs-5 text-body text-nowrap'),
            dbc.CardBody(components.MTA_pred_line, className='p-2'),
        ], className='flex-fill', style={'min-width': 700, 'min-height': 500}),
    ], className='flex-fill w-100 d-flex flex-wrap gap-2'),

], className='flex-fill d-flex flex-column align-items-center gap-2 p-2 overflow-auto dbc-ag-grid')

app.layout = dmc.MantineProvider(
    html.Div([
        title_layout,
        main_layout
    ], className='h-100 d-flex flex-column')
)

# Switch color-theme for DBC and DMC components
clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');
       document.documentElement.setAttribute('data-mantine-color-scheme', switchOn ? 'light' : 'dark');
       return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "checked"),
)

if __name__ == '__main__':
    app.run(debug=True)
