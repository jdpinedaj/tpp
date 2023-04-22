import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Plot the total estimated visits of each venue over time, using both the visit_weight and customer_weight
fig, ax = plt.subplots(2, 1, figsize=(30, 10))
sns.lineplot(data=grouped_visits,
             x='start_date',
             y='visit_weight',
             hue='place',
             ax=ax[0])
sns.lineplot(data=grouped_customers,
             x='start_date',
             y='customer_weight',
             hue='place',
             ax=ax[1])
ax[0].set_title('Total estimated visits over time')
ax[1].set_title('Total estimated customers over time')

# Show the plot in Streamlit
st.pyplot(fig)
