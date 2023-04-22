import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Reading necessary datasets for plotting
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

fig, ax = plt.subplots(2, 1, figsize=(30, 10))
st.pyplot(
    grouped_visits.pivot(index='start_date',
                         columns='place',
                         values='visit_weight').plot(ax=ax[0]))
st.pyplot(
    grouped_customers.pivot(index='start_date',
                            columns='place',
                            values='customer_weight').plot(ax=ax[1]))
