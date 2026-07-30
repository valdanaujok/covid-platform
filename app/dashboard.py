import pandas as pd
import plotly.express as px
import requests

from dash import Dash, Input, Output, dcc, html


# Address of the FastAPI application
API_URL = "http://127.0.0.1:8000"


# Get country names from the API
response = requests.get(
    f"{API_URL}/countries",
    timeout=30,
)

countries = response.json()["countries"]


# Get vaccine names from the API
vaccine_response = requests.get(
    f"{API_URL}/vaccines",
    timeout=30,
)

vaccines = vaccine_response.json()["vaccines"]


# Get vaccine summary data from the API
summary_response = requests.get(
    f"{API_URL}/vaccine-summary",
    timeout=30,
)

vaccine_summary = summary_response.json()["data"]


# Create the vaccine bar chart
vaccine_bar_chart = px.bar(
    vaccine_summary,
    x="vaccine",
    y="country_count",
    title="Number of countries using each vaccine",
    labels={
        "vaccine": "Vaccine",
        "country_count": "Number of countries",
    },
)


# Create the dashboard
app = Dash(__name__)


# Describe what appears on the webpage
app.layout = html.Div(
    [
        html.H1("COVID-19 Dashboard"),

        # Country section
        html.H2("Country information"),

        html.P("Select a country:"),

        dcc.Dropdown(
            id="country-dropdown",
            options=countries,
            value="Lithuania",
            clearable=False,
        ),

        html.H3("Country summary"),

        html.Div(
            id="country-profile"
        ),

        html.H3("Vaccines used by this country"),

        html.P(
            id="country-vaccines"
        ),

        dcc.Graph(
            id="covid-chart"
        ),

        html.Hr(),

        # Vaccine section
        html.H2("Vaccine information"),

        html.P("Select a vaccine:"),

        dcc.Dropdown(
            id="vaccine-dropdown",
            options=vaccines,
            value=vaccines[0],
            clearable=False,
        ),

        html.H3(
            id="vaccine-country-count"
        ),

        html.H4("Countries using this vaccine:"),

        html.Ul(
            id="vaccine-country-list"
        ),

        dcc.Graph(
            id="vaccine-bar-chart",
            figure=vaccine_bar_chart,
        ),
    ]
)


# Update the country section
@app.callback(
    Output("covid-chart", "figure"),
    Output("country-vaccines", "children"),
    Output("country-profile", "children"),
    Input("country-dropdown", "value"),
)
def update_chart(country):

    # Ask FastAPI for the selected country's data
    response = requests.get(
        f"{API_URL}/covid/{country}",
        timeout=30,
    )

    covid_data = response.json()["data"]

    # Convert the API response into a DataFrame
    dataframe = pd.DataFrame(covid_data)

    # Get the latest row
    latest_row = dataframe.iloc[-1]

    # Prepare population for display
    if pd.isna(latest_row["population"]):
        population = "No data"
    else:
        population = (
            f"{int(latest_row['population']):,}"
        )

    # Prepare population density for display
    if pd.isna(latest_row["density_p_km2"]):
        density = "No data"
    else:
        density = (
            f"{int(latest_row['density_p_km2']):,}"
        )

    # Prepare life expectancy for display
    if pd.isna(latest_row["life_expectancy"]):
        life_expectancy = "No data"
    else:
        life_expectancy = (
            f"{float(latest_row['life_expectancy']):.1f}"
        )

    # Prepare healthcare expenditure for display
    if pd.isna(latest_row["health_expenditure"]):
        health_expenditure = "No data"
    else:
        health_expenditure = (
            f"{float(latest_row['health_expenditure']):.2f}%"
        )

    # Create the line chart
    figure = px.line(
        dataframe,
        x="date",
        y=["cases", "deaths"],
        title=f"COVID-19 cases and deaths in {country}",
    )

    # Ask FastAPI for vaccines used by the country
    vaccine_response = requests.get(
        f"{API_URL}/vaccines/{country}",
        timeout=30,
    )

    if vaccine_response.status_code == 200:

        country_vaccines = (
            vaccine_response.json()["vaccines"]
        )

        vaccine_text = ", ".join(country_vaccines)

    else:
        vaccine_text = "No vaccine information available"

    # Create the country profile
    country_profile = [
        html.P(
            f"Latest cases: "
            f"{int(latest_row['cases']):,}"
        ),

        html.P(
            f"Latest deaths: "
            f"{int(latest_row['deaths']):,}"
        ),

        html.P(
            f"Population: {population}"
        ),

        html.P(
            f"Population density: "
            f"{density} people per km²"
        ),

        html.P(
            f"Life expectancy: "
            f"{life_expectancy} years"
        ),

        html.P(
            f"Out-of-pocket healthcare expenditure: "
            f"{health_expenditure}"
        ),
    ]

    return figure, vaccine_text, country_profile


# Update the vaccine section
@app.callback(
    Output("vaccine-country-count", "children"),
    Output("vaccine-country-list", "children"),
    Input("vaccine-dropdown", "value"),
)
def update_vaccine_information(vaccine):

    # Ask FastAPI which countries use the vaccine
    response = requests.get(
        f"{API_URL}/countries-by-vaccine",
        params={"vaccine": vaccine},
        timeout=30,
    )

    countries_using_vaccine = (
        response.json()["countries"]
    )

    # Create the count message
    count_text = (
        f"{len(countries_using_vaccine)} countries "
        f"use {vaccine}"
    )

    # Create the country list
    country_list = []

    for country in countries_using_vaccine:
        country_list.append(
            html.Li(country)
        )

    return count_text, country_list


# Start the dashboard
if __name__ == "__main__":
    app.run(debug=True, port=8050)