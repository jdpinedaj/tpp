import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#! Reading data
# Reading the two datasets for plotting
data = pd.read_csv('output/data.csv')
visits = pd.read_csv('output/visits.csv')

#! Analysis
# Plotting analysis at date level
st.title('Analysis')
st.header('Analysis at date level')
st.subheader(
    'Total estimated visits and customers per Planet Fitness location over time'
)

grouped_visits = visits.groupby(['place', 'start_date']).agg({
    'visit_weight':
    'sum'
}).reset_index()
grouped_customers = data.groupby(['device_id', 'place', 'start_date']).agg({
    'customer_weight':
    'sum'
}).reset_index()

# Plot the total estimated visits of each venue over time, using both the visit_weight and customer_weight
fig, ax = plt.subplots(2, 1, figsize=(50, 10))
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
st.write(
    'These line plots show the total estimated visits of each venue over time.\n Here, we can identify the underperforming venue of Alpharetta in comparison to the other venues.'
)
st.pyplot(fig)

############################################

# Plotting analysis at hour level
st.header('Analysis at hour level')
st.subheader(
    'Total estimated visits and customers per Planet Fitness location at each hour'
)

grouped_visits = visits.groupby(['place', 'visit_hour']).agg({
    'visit_weight':
    'sum'
}).reset_index()
grouped_customers = data.groupby(['device_id', 'place', 'visit_hour']).agg({
    'customer_weight':
    'sum'
}).reset_index()

# Plot the average estimated visits of each venue over time, using both the visit_weight and customer_weight
fig, ax = plt.subplots(2, 1, figsize=(30, 10))
sns.lineplot(data=grouped_visits,
             x='visit_hour',
             y='visit_weight',
             hue='place',
             ax=ax[0])
sns.lineplot(data=grouped_customers,
             x='visit_hour',
             y='customer_weight',
             hue='place',
             ax=ax[1])
ax[0].set_title('Average estimated visits over time')
ax[1].set_title('Average estimated customers over time')

# Show the plot in Streamlit
st.write(
    'These line plots show the average estimated visits of each venue over time.\n Here, we can see that the total estimated visits and customers of alpharetta is lower than the other venues in all periods of the day. Alpharetta only performs well in comparison to the other venues at middays and at 19 h.'
)
st.pyplot(fig)

############################################
