# COVID-19 Data Integration, Analysis, and Visualization Platform

## Project overview
This project is a data platform for exploring COVID-19 information from different countries.
The platform combines COVID-19 epidemiological data from Snowflake with demographic data from a Kaggle CSV file. It also uses MongoDB to store user comments and annotations.
Users can interact with the data through a FastAPI API and a Plotly/Dash dashboard.

### Main features

The current MVP includes:
* Connection between Python and Snowflake.
* COVID-19 data obtained from Snowflake Marketplace.
* Additional demographic data from Kaggle.
* Cleaned and enriched COVID-19 gold table.
* Country and vaccine data queries.
* FastAPI endpoints that return JSON data.
* MongoDB storage for user comments.
* Interactive Dash and Plotly dashboard.
* Country selection using a dropdown.
* Cases and deaths line chart.
* Country population and demographic information.
* Vaccine information for each country.
* List of countries using a selected vaccine.

## Tables

### COVID gold table

The main Snowflake table contains:

* Country
* Continent
* Date
* Confirmed cases
* Deaths
* Population
* Population density
* Birth rate
* Life expectancy
* Out-of-pocket health expenditure

### Country vaccines table
The vaccine table contains:
* Country
* Vaccine

Each country can have several rows because one country may use several vaccine types.

### MongoDB comments
A comment document contains information similar to:

```json
{
  "country": "Country",
  "comment": "Comment.",
  "created_at": "Date"
}
```

## Installation

### Requirements

Before starting the project, install:
    • Python 3
    • Git
    • A Snowflake account
    • Docker

The Snowflake database and tables must already exist and be accessible to the configured Snowflake user.

Please use Linux!

For Windows, you might need to change import on api.py

### Setup
1. Download the project
Clone the GitHub repository:
git clone YOUR_REPOSITORY_URL
cd Covid-platform
Alternatively, download the project as a ZIP file and open the project folder in VS Code.
2. Create a virtual environment
Run these commands from the main project folder:
python3 -m venv .venv
source .venv/bin/activate
The virtual environment keeps the project packages separate from the rest of the computer.
3. Install the dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

### Environment configuration

Add the following settings to .env file:
```
SNOWFLAKE_ACCOUNT=your_snowflake_account
SNOWFLAKE_USER=your_snowflake_user
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=COVID_PROJECT_DB
SNOWFLAKE_SCHEMA=ANALYTICS
SNOWFLAKE_ROLE=your_snowflake_role

MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=covid_project
```
### Running the project

Always run the commands from the main project folder.
* Create python virtual environment (run only once first time)
  ```
  python -m venv .venv
  ```
* Activate the virtual environment
```
source .venv/bin/activate
```
* start up mongoDB with docker
```
docker compose up -d
```
* Test the Snowflake connection
```
python app/snowflake_connection.py
```
A successful result should contain:
Snowflake connection successful!
* Start the FastAPI application
```
python -m uvicorn app.api:app --reload
```
The API will be available at:
http://127.0.0.1:8000
The interactive API documentation is available at:
http://127.0.0.1:8000/docs
Keep this terminal running.
* Start the dashboard
Open a second terminal in the project folder:
```
source .venv/bin/activate
python app/dashboard.py
```
The dashboard will be available at:
http://127.0.0.1:8050

FastAPI must remain running while the dashboard is being used because the dashboard requests its data from the API.

## API endpoints

Go to http://localhost:8000/docs

GET	/ - Confirms that the API is running
GET	/health	- Returns the API health status
GET	/countries - Returns available country names
GET	/covid/{country} - Returns COVID-19 data for one country
GET	/vaccines - Returns the available vaccine names
GET	/vaccines/{country}	- Returns vaccines used by one country
GET	/countries-by-vaccine - Returns countries using a selected vaccine
GET	/vaccine-summary - Returns a summary of vaccine use
GET	/comments - Returns comments stored in MongoDB
POST	/comments - Adds a new comment to MongoDB

Example request:
http://127.0.0.1:8000/covid/Lithuania
Example vaccine request:
http://127.0.0.1:8000/vaccines/Lithuania

## Dashboard features

The dashboard allows a user to:
* Select a country.
* View cases and deaths over time.
* View information such as population, density and life expectancy.
* View the vaccines used in the selected country.
* Select a vaccine.
* View countries that used the selected vaccine.
* http://localhost:8000/docsView a vaccine summary chart.

Plotly creates the charts, while Dash provides the webpage, dropdowns and interactive callbacks.
Testing on another computer

## Data exploration
Exploratory data analysis was used to understand:
* Available columns.
* Number of rows.
* Date range.
* Number of countries.
* Missing values.
* Duplicate values.
* Basic statistics.
* Cases and deaths by country.
EDA helps find problems in the data before the data is used by the API and dashboard.

## Technologies used
* Snowflake – stores COVID-19, demographic and vaccine data.
* FastAPI – provides API endpoints.
* MongoDB – stores comments and annotations.
* Dash – creates the interactive web application.
* Plotly – creates the charts displayed by Dash.

