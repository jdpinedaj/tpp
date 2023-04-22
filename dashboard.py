import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from utils import (
    analysis_date_level,
    analysis_hour_level,
    analysis_day_week_level,
    analysis_weekend_level,
    analysis_month_level,
    analysis_distance_from_home_level,
    analysis_distance_from_work_level,
    map_venue,
)

#! Reading data
# Reading the two datasets for plotting
data = pd.read_csv('output/data.csv')
visits = pd.read_csv('output/visits.csv')
customers = pd.read_csv('output/customers.csv')
customers_alpharetta = pd.read_csv('output/customers_alpharetta.csv')
customers_highway = pd.read_csv('output/customers_highway.csv')
customers_holcomb = pd.read_csv('output/customers_holcomb.csv')
customers_molly = pd.read_csv('output/customers_molly.csv')

#! Analysis
st.title('Analysis')
############################################
# Plotting analysis at date level
analysis_date_level(data, visits)

############################################
# Plotting analysis at hour level
analysis_hour_level(data, visits)
############################################

############################################

# Plotting analysis at day of week level
analysis_day_week_level(data, visits)

############################################

# Plotting analysis at weekend level
analysis_weekend_level(data, visits)

############################################

# Plotting analysis at month level
analysis_month_level(data, visits)

############################################

# Plotting analysis at distance from home level
analysis_distance_from_home_level(data, visits)

############################################

# Plotting analysis at distance from work level
analysis_distance_from_work_level(data, visits)

############################################

#! Geo-location analysis

# Plotting analysis at geo-location level
# Alpharetta
map_venue(customers, customers_alpharetta, 'blue')