import pandas as pd
import dash_leaflet as dl
import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output, dcc, State, ALL, dash
from dash_extensions.javascript import arrow_function, Namespace
from dash_extensions import EventListener
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import plotly.express as px

import util

ns = Namespace("dashExtensions", "default")

geophysical_icon = html.Img(
    src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAAC+klEQVR4nO2YS2gTURRAnz9EFxYUhWrIvTNE3biR+lsU60YpiNRNaOfdiQuRrtyJ61YQFHXlUtwoVcRFwYWflaWWdu4bY8EPqF2JgqAIivhF28jLTEzSX5IyyczAHHiQzJvFPXPf574nREJCQkLCPBSEWCbiDlP6sGNBn4gz+f6OVSzhlSKYGukSK0VcURJOKcKCbkxwXMSRcdvcxBI/l0QUwZup7sxqETeY4IqXCbynCJ4Wf9vGSREn3D7YqQj/MsFvl3A723C0KCLxfb6/fa2IC0ww6g+ni6VnSgL7GTot4oBjQV9RQsKHfNZsKz1nwkN+Vj4xZdaJKDORTa3Rk9rLhnFidr+SOOLLDIgoowgG/eEzeTsrVszudyyz01+Kv6jc5g0iijBlUizxmzescP/C78EDX+a8iCJMcMuXuLnoezLdwYQzivDHxLHUFhElHMvs1MGxxO/5nJmu9T5LHPbmClwWUaEwIJYriU/85Xawsk/v5IrgupJwprICdm1zB0ucZgm/6hFvCXp1KtdTOFQqQyayqfXl/aS6T090Jnjr910VYZPPmm16vyjXU8X94xET7GMJr6ueexkbm9sHfxzL3NqyoB2CA7oQrHzGhJfmBtt4Y8IbLZHQZwn9FVnC85KMyhnbdC0ViIjEaT1vmi7CEvsrvt7LPKXbFeHdICQqZIabX3ZIeDdrHlT/D2Z4zaicuatpIrpaDTroRbJyv2mrkq5WWyWiCAuuhV2Bi7DEs62UUMUGY4FKTGYzG5WEr60XwYJjGwcDE9F1UBgSyqvB3FJJ49i417WMI0uScHoBdR0UlojyJn6PLmmY8IXew/QdWcMiSsK1MCWUN1eeKQkX/os1egOjd1h9AxK+CFZniOBj5R1APdm4E3bQauHhdq4uiceWscc/vRUi2ST+HJcItbNB+DD0YKnWEMOhxSVs6A47SFWfyIxLxu55JfSaXT6uRr8xwei8Iq7E3rCDU43KSOypktAXafqMET8RWNommZCQkJCQIKr5B4e3yC7b0qbRAAAAAElFTkSuQmCC", style={"width": "auto", "height": "24px"})
meteorological_icon = html.Img(
    src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAxElEQVR4nO3UPWpCQRiF4cdGXYN2rsBNWIkuJKhlNiCmyZrEMj9NIuIybDSCNk4YuQS5GOWqQwh44FQD75k538dw139QDSO8Y4E1ZnhG41r4A7YIvziePV4KfzoBzju+ppBa2BUIiO6eg5bRxys2BeEBc5RODXJ6ATTk3DwGr+LzBvCAFSboHAYMbgQPOcfV3ustUUBAOwZ8JQwYy3pLFbBMXdFStvtJK6rgI+WQo+oJQoaOfBU9vFwx+FVWy8/N7/p7fQOe/B+BqqKyIgAAAABJRU5ErkJggg==", style={"width": "auto", "height": "24px"})
hydrological_icon = html.Img(
    src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAABTElEQVR4nM2VO0sDQRDHrxAfxJ07bAQ7sbLwUfsZ7PxI+QA+GjEfwSZF4swqQtTCLt1hIciZmUNr0WChl8idFxIQ3UcScOAPVyy/3+7scBsE/6lCLXt5pgJXOt0BlPc8+fdE4ZXLh2UgSYGkX+Z54aKzMhl6qz8DJNcj8O8g3wan8ezYfEA+/AEfSg7Ggiud7v4KL5Ov8YKH9SRSxGISAMoTaF5y3z1xzQgfnIK45gRfbCbrgPxhKwDiz8oZb1gLALlhD5fBhTes4OH54yoQZx6CHmBnzShQKFVnOJV3gVK1EHDbX8Bts4C46y0g7tqc4NVfIC9GARDf+QoAJbZokRx5C4j3jYKwmW57jSlxFqFsGgWuvwkYTtBxYF2tZB5QbhwEVwHez9kLSokiPvm7XZwVO3eGj1SkZat4dFBihfxWjDFKnD821j2fZn0BzxejKOBMlnUAAAAASUVORK5CYII=", style={"width": "auto", "height": "24px"})
climatological_icon = html.Img(
    src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAABIUlEQVR4nOVVW04CQRCsQ4gHM3gF8RogF8CDAAcQf30kggehRnfg2zLTLjjgZkKv7peTdLLZna7qrtmuARxLAc8KeERXSwFK0SXBkwIe2gMQ1yLmiui5cyPORMxEDEoEM5OBWLQo7r7OnZaq6Im4EzHZv9vgXMRYxEoBWwtiKeImfcsIJpbr6V7EpQLi7nAbImqNvrfbb3DiowD+FWmPl8RkKVeuo6i80owd4Ko7GXkIXlsQLEvjr9wCnPJod+CNmPV0Kp/QlgRVlv8D81ii1Z9J1LRsiPwEwy5/0/fkRScTGMka/ZMH7Q0XLvADkoCqWLkHvLbcxYHZRTPAkYgXBWws0jMxzGURcWu5Jam6t2tikDb84sKZirjy5mIP8i8v/U/2bn/Cuda4GwAAAABJRU5ErkJggg==", style={"width": "auto", "height": "24px"})

show_events_button = dbc.Button(
    "Show all events", color="primary", className="me-1 show-events", id="world-show-events")

world_slider = dcc.Slider(min=1960,
                          max=2023,
                          step=1,
                          value=1960,
                          marks=None,
                          tooltip={"placement": "bottom",
                                   "always_visible": True},
                          id="world-year-slider",
                          className="slider")

animation_button = dbc.Button(children=[
    "Play",
    DashIconify(
        icon="material-symbols:play-arrow-rounded"
    )
],
    color="success",
    class_name="me-1",
    id="world-animation-button")

animation_interval = dcc.Interval(
    'animation-interval', interval=500, disabled=True)

world_slider_wrapper = EventListener(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        animation_button
                    ],
                    className="column",
                    width="auto"),
                dbc.Col(
                    children=[
                        world_slider
                    ],
                    className="column"),
                animation_interval
            ], className="slider-container")
    ], id="world-slider-wrapper", events=[{"event": "mouseout", "props": ["type"]}, {"event": "mouseover", "props": ["type"]}])

map_legend = html.Div(children=[
    dbc.Col(children=[
        dbc.Row(children=[
            dbc.Col(children=[
                geophysical_icon
            ]),
            dbc.Col(children=[
                html.P("Geophysical", className="map-legend-item-text")
            ], className="map-legend-item")
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                meteorological_icon
            ]),
            dbc.Col(children=[
                html.P("Meteorological", className="map-legend-item-text")
            ], className="map-legend-item")
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                hydrological_icon
            ]),
            dbc.Col(children=[
                html.P("Hydrological", className="map-legend-item-text")
            ], className="map-legend-item")
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                climatological_icon
            ]),
            dbc.Col(children=[
                html.P("Climatological", className="map-legend-item-text")
            ], className="map-legend-item")
        ])
    ], className="map-legend-item-wrapper")
], className="map-legend")

map = dl.Map(
    maxBounds=[[-90, -180], [90, 180]],
    maxBoundsViscosity=1.0,
    maxZoom=18,
    minZoom=2,
    center=(40, -37),
    bounceAtZoomLimits=True,
    children=[
        dl.TileLayer(),
        # https://datahub.io/core/geo-countries#resource-countries
        dl.GeoJSON(
            data=util.get_world_geojson(),
            id="countries",
            # Invisible polygons,
            options={"style": {"color": "transparent"}},
            zoomToBounds=True,
            hoverStyle=arrow_function(dict(weight=3, color='#666', dashArray=''))),  # Gray border on hover (line_thickness, color, line_style)
        dl.GeoJSON(data={},
                   id="events",
                   options=dict(pointToLayer=ns("draw_marker"))),
        map_legend,
        world_slider_wrapper
    ],
    style={"width": "100%", "height": "100%", "display": "block"},
    id="map")

world_gdp_graph = dcc.Graph(
    id="world-gdp-graph", style={"height": "30vh", "width": "100%"})
world_affected_graph = dcc.Graph(
    id="world-affected-graph", style={"height": "30vh", "width": "100%"})

home_layout = html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Card(
                            children=[
                                dbc.CardHeader(
                                    children=[
                                        "World Map"
                                    ]
                                ),
                                dbc.CardBody(
                                    children=[
                                        map
                                    ]
                                )
                            ],
                            className="map-card")
                    ],
                    width=9,
                    className="column map-column"),
                dbc.Col(
                    children=[
                        dbc.Card(
                            children=[
                                dbc.CardHeader(
                                    children=[
                                        "Aggregated Data"
                                    ]
                                ),
                                dbc.CardBody(
                                    children=[
                                        html.Div(
                                            id="world-aggregated-data"),
                                        show_events_button
                                    ]
                                )
                            ],
                            className="aggregated-card")
                    ],
                    width=3,
                    className="column aggregated-column")
            ],
            className="map-row"
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Card(
                            children=[
                                dbc.CardHeader(
                                    children=[
                                        "GDP Data"
                                    ]
                                ),
                                dbc.CardBody(
                                    children=[
                                        dbc.Tabs(
                                            children=[
                                                dbc.Tab(
                                                    label="General", tab_id="general"),
                                                dbc.Tab(
                                                    label="Specific", tab_id="specific"),
                                            ],
                                            id="world-gdp-tabs",
                                            active_tab="general"
                                        ),
                                        world_gdp_graph
                                    ],
                                    className="gdp-cardbody")
                            ],
                            className="gdp-card")
                    ],
                    width=6,
                    className="column gdp-column"),
                dbc.Col(
                    children=[
                        dbc.Card(
                            children=[
                                dbc.CardHeader(
                                    children=[
                                        "Affected Data"
                                    ]
                                ),
                                dbc.CardBody(
                                    children=[
                                        dbc.Tabs(
                                            children=[
                                                dbc.Tab(
                                                    label="Total Deaths", tab_id="deaths"),
                                                dbc.Tab(
                                                    label="Total Injured", tab_id="injuries"),
                                                dbc.Tab(
                                                    label="Total Homeless", tab_id="homeless")
                                            ],
                                            id="world-affected-tabs",
                                            active_tab="deaths"
                                        ),
                                        world_affected_graph
                                    ]
                                )
                            ],
                            className="affected-card")
                    ],
                    width=6,
                    className="column affected-column")
            ],
            className="graphs-row"),
            html.Div(
                    children=[
                        dbc.Offcanvas(
                            children=[
                                dbc.Accordion(
                                    id="world-events-accordion"
                                )
                            ],
                            is_open=False,
                            placement="end",
                            id="world-offcanvas"
                        )
                    ]
                )
    ],
    id="home"
)