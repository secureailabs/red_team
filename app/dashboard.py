import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from app.data_generator import PATIENT_DF

colors = {"background": "#111111", "text": "#7FDBFF"}


def create_dashboard(server):
    app = Dash(
        server=server,
        routes_pathname_prefix="/pag/dashboard/",
        # external_stylesheets=[],
    )
    data = filter_df(PATIENT_DF)
    app = fill_layout(app, data)
    app = init_callbacks(app)
    return app.server


def filter_df(df, yearmin=2013, yearmax=2022, agemin=0, agemax=150, gender=None):
    if gender is not None:
        df = df[df["gender"] == gender]

    df = df[df["age"] <= agemax]
    df = df[df["age"] >= agemin]

    df = df[df["year"] <= yearmax]
    df = df[df["year"] >= yearmin]

    data = df["state"].value_counts()

    new_df = pd.DataFrame()
    new_df["state"] = data.index
    new_df["count"] = data.values
    new_df["text"] = new_df["state"] + ":" + new_df["count"].astype(str)
    return new_df


def get_map(data):
    fig = go.Figure(
        data=go.Choropleth(
            locations=data["state"],
            z=data["count"].astype(float),
            locationmode="USA-states",
            colorscale="Viridis",
            text=data["text"],
            colorbar_title="Number of cases",
        )
    )
    fig.update_layout(
        geo_scope="usa",
    )
    return fig


def get_age_histogram(df, state=None):
    if state is not None:
        df = df[df["state"] == state]

    male_df = df[df["gender"] == "male"]
    female_df = df[df["gender"] == "female"]

    figure = go.Figure()

    figure.add_trace(
        go.Histogram(
            x=male_df["age"],
            histnorm="percent",
            name="male",
            xbins=dict(start=40, end=100, size=5),
            marker_color="#EB89B5",
            opacity=0.75,
        )
    )
    figure.add_trace(
        go.Histogram(
            x=female_df["age"],
            histnorm="percent",
            name="female",
            xbins=dict(start=40, end=100, size=5),
            marker_color="#330C73",
            opacity=0.75,
        )
    )
    figure.update_layout(
        title_text="patient age distribution histogram",
        xaxis_title_text="Age",
        yaxis_title_text="Count",
        bargap=0.2,
        bargroupgap=0.1,
        paper_bgcolor="#F4F4F8",
        plot_bgcolor="#F4F4F8",
        margin=dict(t=75, r=50, b=100, l=50),
    )
    return figure


def get_year_case_graph(df, state=None):
    if state is not None:
        df = df[df["state"] == state]

    male_df = df[df["gender"] == "male"]
    female_df = df[df["gender"] == "female"]

    male_data = male_df["year"].value_counts()
    female_data = female_df["year"].value_counts()
    male_data.sort_index(inplace=True)
    female_data.sort_index(inplace=True)

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=male_data.index,
            y=male_data.values,
            mode="lines+markers",
            name="male",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=female_data.index,
            y=female_data.values,
            mode="lines+markers",
            name="female",
        )
    )
    figure.update_layout(
        title="yearly reported diagnostic cases number",
        xaxis_title="Year",
        yaxis_title="Case number",
        paper_bgcolor="#F4F4F8",
        plot_bgcolor="#F4F4F8",
        margin=dict(t=75, r=50, b=100, l=50),
    )
    return figure


def get_patient_symptom_graph(df, state=None):
    if state is not None:
        df = df[df["state"] == state]

    symptoms = [
        "Depression",
        "Moode swing",
        "Change in sleeping habits",
        "Unawared wandering at night",
        "Distrust on other people",
    ]
    yes_symptoms = [
        df["Depression"].value_counts()[0],
        df["Moode swing"].value_counts()[0],
        df["Change in sleeping habits"].value_counts()[0],
        df["Unawared wandering at night"].value_counts()[0],
        df["Distrust on other people"].value_counts()[0],
    ]
    no_symptoms = [
        df["Depression"].value_counts()[1],
        df["Moode swing"].value_counts()[1],
        df["Change in sleeping habits"].value_counts()[1],
        df["Unawared wandering at night"].value_counts()[1],
        df["Distrust on other people"].value_counts()[1],
    ]

    figure = go.Figure()
    figure.add_trace(go.Bar(x=symptoms, y=yes_symptoms, name="yes", marker_color="indianred"))
    figure.add_trace(go.Bar(x=symptoms, y=no_symptoms, name="no", marker_color="lightsalmon"))
    figure.update_layout(
        barmode="group",
        xaxis_tickangle=-45,
        paper_bgcolor="#F4F4F8",
        plot_bgcolor="#F4F4F8",
        margin=dict(t=75, r=50, b=100, l=50),
    )
    return figure


def fill_layout(app, data):
    app.layout = html.Div(
        children=[
            html.H4(children="Altzheimer's disease statistics based on aggreagated patient diagnosis"),
            html.Div(
                children=[
                    dcc.RangeSlider(
                        id="year-slider",
                        min=2013,
                        max=2022,
                        value=[2013, 2022],
                        step=1,
                        marks={
                            str(year): {
                                "label": str(year),
                                "style": {"color": "#7fafdf"},
                            }
                            for year in range(2013, 2023)
                        },
                    ),
                    html.Br(),
                    dcc.RangeSlider(
                        id="age-range",
                        min=40,
                        max=100,
                        step=5,
                        value=[40, 100],
                    ),
                    html.Br(),
                    dcc.Checklist(
                        id="gender-select",
                        options=["male", "female"],
                        value=["male", "female"],
                    ),
                    html.Br(),
                ]
            ),
            html.Div(
                children=[
                    html.P("Heat map of number of Altzheimer cases reported as primary diagnosis in US"),
                    dcc.Graph(
                        id="us-choropleth",
                        figure=get_map(data),
                    ),
                ]
            ),
            html.Div(
                children=[
                    html.P("Please select a chart to displace"),
                    dcc.Dropdown(
                        options=[
                            {"label": "patient age distribution histogram", "value": "age_histogram"},
                            {"label": "yearly reported diagnostic cases number", "value": "year_case_number"},
                            {"label": "patient symptoms histogram", "value": "patient_symptoms_histogram"},
                        ],
                        value="age_histogram",
                        id="chart-dropdown",
                    ),
                    dcc.Graph(
                        id="selected-data",
                        figure=dict(
                            data=[dict(x=0, y=0)],
                            layout=dict(paper_bgcolor="#F4F4F8", plot_bgcolor="#F4F4F8", height=700),
                        ),
                    ),
                ]
            ),
        ]
    )
    return app


def init_callbacks(app):
    @app.callback(
        Output("us-choropleth", "figure"),
        [
            Input("year-slider", "value"),
            Input("age-range", "value"),
            Input("gender-select", "value"),
        ],
    )
    def load_map(year, age_range, gender):
        yearmin, yearmax = year[0], year[1]
        agemin, agemax = age_range[0], age_range[1]
        if len(gender) == 2:
            gender = None
        else:
            gender = gender[0]

        data = filter_df(PATIENT_DF, yearmin, yearmax, agemin, agemax, gender)

        fig = get_map(data)
        return fig

    @app.callback(
        Output("selected-data", "figure"),
        [
            Input("chart-dropdown", "value"),
            Input("us-choropleth", "selected"),
        ],
    )
    def load_figure(chart_name, state):
        if chart_name == "age_histogram":
            return get_age_histogram(PATIENT_DF, state)
        elif chart_name == "year_case_number":
            return get_year_case_graph(PATIENT_DF, state)
        else:
            return get_patient_symptom_graph(PATIENT_DF, state)

    return app
