import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Reading the two datasets for plotting
data = pd.read_csv('output/data.csv')
visits = pd.read_csv('output/visits.csv')

# Plotting analysis at date level
st.title('Analysis at Date Level')

grouped_visits = visits.groupby(['place', 'start_date']).agg({
    'visit_weight':
    'sum'
}).reset_index()
grouped_customers = data.groupby(['device_id', 'place', 'start_date']).agg({
    'customer_weight':
    'sum'
}).reset_index()

# Plotting visits
fig, ax = plt.subplots(figsize=(30, 10))
grouped_visits.pivot(index='start_date',
                     columns='place',
                     values='visit_weight').plot(ax=ax)
st.pyplot(fig)

# Plotting customers
fig, ax = plt.subplots(figsize=(30, 10))
grouped_customers.pivot(index='start_date',
                        columns='place',
                        values='customer_weight').plot(ax=ax)
st.pyplot(fig)
