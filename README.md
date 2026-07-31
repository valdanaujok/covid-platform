COVID-19 Data Integration, Analysis, and Visualization Platform

Project overview
This project is a data platform for exploring COVID-19 information from different countries.
The platform combines COVID-19 epidemiological data from Snowflake with demographic data from a Kaggle CSV file. It also uses MongoDB to store user comments and annotations.
Users can interact with the data through a FastAPI API and a Plotly/Dash dashboard.

Project architecture

Technologies used
    • Snowflake – stores COVID-19, demographic and vaccine data.
    • Python – connects and processes the different parts of the project.
    • Pandas – works with tabular data.
    • FastAPI – provides API endpoints.
    • MongoDB Atlas – stores comments and annotations.
    • Dash – creates the interactive web application.
    • Plotly – creates the charts displayed by Dash.
    • Requests – allows the dashboard to request data from FastAPI.
    • python-dotenv – loads configuration from the .env file.

Main features

The current MVP includes:
    • Connection between Python and Snowflake.
    • COVID-19 data obtained from Snowflake Marketplace.
    • Additional demographic data from Kaggle.
    • Cleaned and enriched COVID-19 gold table.
    • Country and vaccine data queries.
    • FastAPI endpoints that return JSON data.
    • MongoDB storage for user comments.
    • Interactive Dash and Plotly dashboard.
    • Country selection using a dropdown.
    • Cases and deaths line chart.
    • Country population and demographic information.
    • Vaccine information for each country.
    • List of countries using a selected vaccine.

Project structure

Covid-platform/
├── app/
│   ├── api.py
│   ├── dashboard.py
│   ├── eda.py
│   ├── main.py
│   ├── mongodb.py
│   └── snowflake_connection.py
├── data/
│   └── world_data.csv
├── sql/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt

COVID gold table

The main Snowflake table contains:
    • Country
    • Continent
    • Date
    • Confirmed cases
    • Deaths
    • Population
    • Population density
    • Birth rate
    • CO2 emissions
    • Life expectancy
    • Out-of-pocket health expenditure

Country vaccines table
The vaccine table contains:
    • Country
    • Vaccine

Each country can have several rows because one country may use several vaccine types.

MongoDB comments
A comment document contains information similar to:

{
  "country": "Country",
  "comment": "Comment.",
  "created_at": "Date"
}

Requirements

Before starting the project, install:
    • Python 3
    • Git
    • A Snowflake account
    • A MongoDB Atlas account

The Snowflake database and tables must already exist and be accessible to the configured Snowflake user.

Installation
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

Environment configuration

The project uses a .env file for passwords and connection settings.
Create it from the example:
cp .env.example .env

Add the following settings:
SNOWFLAKE_ACCOUNT=your_snowflake_account
SNOWFLAKE_USER=your_snowflake_user
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=COVID_PROJECT_DB
SNOWFLAKE_SCHEMA=ANALYTICS
SNOWFLAKE_ROLE=your_snowflake_role

MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DATABASE=covid_project

Do not upload the real .env file to GitHub.
The .gitignore file should contain:
.env
.venv/
__pycache__/
*.pyc

MongoDB Atlas configuration

MongoDB Atlas only accepts connections from permitted IP addresses.
To allow a new computer:
    1. Sign in to MongoDB Atlas.
    2. Open Network Access.
    3. Select Add IP Address.
    4. Add the current computer’s IP address.
    5. Save the changes.

Running the project

Always run the commands from the main project folder.
1. Activate the virtual environment
source .venv/bin/activate
2. Test the Snowflake connection
python app/snowflake_connection.py
A successful result should contain:
Snowflake connection successful!
3. Start the FastAPI application
python -m uvicorn app.api:app --reload
The API will be available at:
http://127.0.0.1:8000
The interactive API documentation is available at:
http://127.0.0.1:8000/docs
Keep this terminal running.
4. Start the dashboard
Open a second terminal in the project folder:
source .venv/bin/activate
python app/dashboard.py

The dashboard will be available at:
http://127.0.0.1:8050

FastAPI must remain running while the dashboard is being used because the dashboard requests its data from the API.

API endpoints

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
Dashboard features

The dashboard allows a user to:
    1. Select a country.
    2. View cases and deaths over time.
    3. View information such as population, density and life expectancy.
    4. View the vaccines used in the selected country.
    5. Select a vaccine.
    6. View countries that used the selected vaccine.
    7. View a vaccine summary chart.

Plotly creates the charts, while Dash provides the webpage, dropdowns and interactive callbacks.
Testing on another computer

The project can be tested on another computer or a clean virtual machine.
Testing steps:
    1. Clone or copy the project.
    2. Create a new virtual environment.
    3. Install requirements.txt.
    4. Create a new .env file.
    5. Add the computer’s IP address to MongoDB Atlas.
    6. Test the Snowflake connection.
    7. Start FastAPI.
    8. Test the endpoints through /docs.
    9. Start Dash.
    10. Test the dropdowns and charts.
Do not copy the original .venv directory because it may contain paths that only exist on the original computer.

To search for computer-specific paths, run:
grep -R "/home/bootcamp-faculty" app README.md --exclude-dir=__pycache__

The command should ideally return no results.

Data exploration
Exploratory data analysis was used to understand:
    • Available columns.
    • Number of rows.
    • Date range.
    • Number of countries.
    • Missing values.
    • Duplicate values.
    • Basic statistics.
    • Cases and deaths by country.
EDA helps find problems in the data before the data is used by the API and dashboard.

Security
    • Passwords are stored in .env.
    • .env is excluded from Git.
    • Real credentials should never appear in source code.
    • A restricted Snowflake user should be used for deployment.
    • Only necessary IP addresses should be allowed in MongoDB Atlas.

