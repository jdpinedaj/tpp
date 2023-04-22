import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium


#! ANALYSIS
def analysis_date_level(data: pd.DataFrame, visits: pd.DataFrame) -> None:
    """
    This function plots the analysis at date level.
    Args:
        data (pd.DataFrame): Dataframe with the data.
        visits (pd.DataFrame): Dataframe with the visits.
    Returns:
        Analysis at date level.
    """
    # Plotting analysis at date level
    st.header('Analysis at date level')
    st.subheader(
        'Total estimated visits and customers per Planet Fitness location over time'
    )

    # Grouping data
    grouped_visits = visits.groupby(['place', 'start_date']).agg({
        'visit_weight':
        'sum'
    }).reset_index()
    grouped_customers = data.groupby(['device_id', 'place',
                                      'start_date']).agg({
                                          'customer_weight':
                                          'sum'
                                      }).reset_index()

    # Plotting
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
        'These line plots show the total estimated visits and customers of each gym per date.'
        +
        ' Here, we can identify the underperforming gym of Alpharetta in comparison to the other gyms.'
    )
    st.pyplot(fig)


def analysis_hour_level(data: pd.DataFrame, visits: pd.DataFrame) -> None:
    """
    This function plots the analysis at hour level.
    Args:
        data (pd.DataFrame): Dataframe with the data.
        visits (pd.DataFrame): Dataframe with the visits.
    Returns:
        Analysis at hour level.
    """
    st.header('Analysis at hour level')
    st.subheader(
        'Total estimated visits and customers per Planet Fitness location at each hour'
    )

    # Grouping data
    grouped_visits = visits.groupby(['place', 'visit_hour']).agg({
        'visit_weight':
        'sum'
    }).reset_index()
    grouped_customers = data.groupby(['device_id', 'place',
                                      'visit_hour']).agg({
                                          'customer_weight':
                                          'sum'
                                      }).reset_index()

    # Plotting
    fig, ax = plt.subplots(2, 1, figsize=(50, 10))
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
        'These line plots show the average estimated visits and customers of each gym per hour.'
        +
        ' Here, we can see that the total estimated visits and customers of alpharetta is lower than the other gyms in all periods of the day. Alpharetta only performs well in comparison to the other gyms at middays and at 19 h.'
    )
    st.pyplot(fig)


def analysis_day_week_level(data: pd.DataFrame, visits: pd.DataFrame) -> None:
    """
    This function plots the analysis at day week level.
    Args:
        data (pd.DataFrame): Dataframe with the data.
        visits (pd.DataFrame): Dataframe with the visits.
    Returns:
        Analysis at day week level.
    """
    st.header('Analysis at day of week level')
    st.subheader(
        'Total estimated visits and customers per Planet Fitness location at each day of the week'
    )

    # Grouping data
    categories_order = [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
        'Sunday'
    ]

    grouped_visits = visits.groupby(['place', 'day_of_week']).agg({
        'visit_weight':
        'sum'
    }).reset_index()
    grouped_customers = data.groupby(['device_id', 'place',
                                      'day_of_week']).agg({
                                          'customer_weight':
                                          'sum'
                                      }).reset_index()

    grouped_visits['day_of_week'] = pd.Categorical(
        grouped_visits['day_of_week'],
        categories=categories_order,
        ordered=True)
    grouped_customers['day_of_week'] = pd.Categorical(
        grouped_customers['day_of_week'],
        categories=categories_order,
        ordered=True)

    # Plotting
    fig, ax = plt.subplots(2, 1, figsize=(50, 10))
    sns.lineplot(data=grouped_visits,
                 x='day_of_week',
                 y='visit_weight',
                 hue='place',
                 ax=ax[0])
    sns.lineplot(data=grouped_customers,
                 x='day_of_week',
                 y='customer_weight',
                 hue='place',
                 ax=ax[1])
    ax[0].set_title('Average estimated visits over time')
    ax[1].set_title('Average estimated customers over time')

    # Show the plot in Streamlit
    st.write(
        'These line plots show the average estimated visits of each gym per week day.'
        +
        ' Here, we can see that the total estimated visits and customers of alpharetta is lower than the other gyms for all days of the week.'
    )
    st.pyplot(fig)


def analysis_weekend_level(data: pd.DataFrame, visits: pd.DataFrame) -> None:
    """
    This function plots the analysis at weekend level.
    Args:
        data (pd.DataFrame): Dataframe with the data.
        visits (pd.DataFrame): Dataframe with the visits.
    Returns:
        Analysis at weekend level.
    """
    st.header('Analysis at weekend level')
    st.subheader(
        'Total estimated visits and customers per Planet Fitness location per weekend'
    )

    # Grouping data
    grouped_visits = visits.groupby(['place', 'weekend']).agg({
        'visit_weight':
        'sum'
    }).reset_index()
    grouped_customers = data.groupby(['device_id', 'place', 'weekend']).agg({
        'customer_weight':
        'sum'
    }).reset_index()

    # Plotting
    fig, ax = plt.subplots(2, 1, figsize=(50, 10))
    sns.barplot(data=grouped_visits,
                x='weekend',
                y='visit_weight',
                hue='place',
                ax=ax[0])
    sns.barplot(data=grouped_customers,
                x='weekend',
                y='customer_weight',
                hue='place',
                ax=ax[1])
    ax[0].set_title('Average estimated visits over time')
    ax[1].set_title('Average estimated customers over time')

    # Show the plot in Streamlit
    st.write(
        'These bar plots show the average estimated visits of each gym per weekend.'
    )
    st.write(
        'Here, we can see that the total estimated visits and customers of alpharetta is lower than the other venues for week days and weekends.'
        +
        ' There is only one exception, which is the total estimated customers and visits of alpharetta at weekdays in comparison to higways.'
    )
    st.pyplot(fig)


def analysis_month_level(data: pd.DataFrame, visits: pd.DataFrame) -> None:
    """
    This function plots the analysis at month level.
    Args:
        data (pd.DataFrame): Dataframe with the data.
        visits (pd.DataFrame): Dataframe with the visits.
    Returns:
        Analysis at month level.
    """
    st.header('Analysis at month level')
    st.subheader(
        'Total estimated visits and customers per Planet Fitness location per month'
    )

    # Grouping data
    categories_order = [
        'January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December'
    ]

    grouped_visits = visits.groupby(['place', 'month']).agg({
        'visit_weight':
        'sum'
    }).reset_index()
    grouped_customers = data.groupby(['device_id', 'place', 'month']).agg({
        'customer_weight':
        'sum'
    }).reset_index()

    grouped_visits['month'] = pd.Categorical(grouped_visits['month'],
                                             categories=categories_order,
                                             ordered=True)
    grouped_customers['month'] = pd.Categorical(grouped_customers['month'],
                                                categories=categories_order,
                                                ordered=True)

    # Plotting
    fig, ax = plt.subplots(2, 1, figsize=(50, 10))
    sns.lineplot(data=grouped_visits,
                 x='month',
                 y='visit_weight',
                 hue='place',
                 ax=ax[0])
    sns.lineplot(data=grouped_customers,
                 x='month',
                 y='customer_weight',
                 hue='place',
                 ax=ax[1])
    ax[0].set_title('Average estimated visits over time')
    ax[1].set_title('Average estimated customers over time')

    # Show the plot in Streamlit
    st.write(
        'These line plots show the average estimated visits of each gym per month.'
        +
        ' We can see that the total estimated visits and customers of alpharetta is lower than the other venues for all months of the year.'
        +
        ' There is only one month in which Alpharetta performs decently in comparison to the other venues, and that is in the month of September.'
    )
    st.pyplot(fig)


def analysis_distance_from_home_level(data: pd.DataFrame,
                                      visits: pd.DataFrame) -> None:
    """
    This function plots the analysis at distance from home level.
    Args:
        data (pd.DataFrame): Dataframe with the data.
        visits (pd.DataFrame): Dataframe with the visits.
    Returns:
        Analysis at distance from home level.
    """
    st.header('Analysis at distance from home level')
    st.subheader(
        'Total estimated visits and customers per Planet Fitness location per distance from home'
    )

    # Grouping data
    grouped_visits = visits.groupby(['place',
                                     'distance_from_home_miles']).agg({
                                         'visit_weight':
                                         'sum'
                                     }).reset_index()
    grouped_customers = data.groupby(
        ['device_id', 'place', 'distance_from_home_miles']).agg({
            'customer_weight':
            'sum'
        }).reset_index()

    # Plotting
    fig, ax = plt.subplots(2, 1, figsize=(50, 10))
    sns.kdeplot(data=grouped_visits,
                x='distance_from_home_miles',
                hue='place',
                fill=True,
                ax=ax[0])
    sns.kdeplot(data=grouped_customers,
                x='distance_from_home_miles',
                hue='place',
                fill=True,
                ax=ax[1])
    ax[0].set_title('Distribution of distance from home for visits')
    ax[1].set_title('Distribution of distance from home for customers')

    # Show the plot in Streamlit
    st.write(
        'These KDE plots show the distribution of distance from home for each gym.'
        +
        ' We can see that the total estimated visits and customers of alpharetta is lower than the other venues for all distances from home.'
        +
        ' The conclusion drawn from the data is that the distribution of customers distance from home to Planet Fitness in Alpharetta is more evenly spread out compared to the distribution of visits. The distribution of visits shows a significant increase for those who live closer to Planet Fitness in Alpharetta, indicating that customers who live in closer proximity to Planet Fitness in in Alpharetta are more likely to attend the gym frequently compared to those who live farther away.'
        +
        ' This observation is interesting because it suggests that proximity to the gym is a significant factor in the frequency of visits by customers. People who live close to the gym may find it more convenient to attend the gym regularly, while those who live farther away may face more obstacles, such as transportation issues (?), that limit their ability to visit frequently.'
        +
        ' Overall, this insight can be valuable for Planet Fitness as it can help them optimize their marketing efforts and target potential customers who live in the nearby areas. Additionally, the gym can also consider offering transportation or other incentives to customers who live farther away (free parking?, more parking cells?) to encourage them to visit more frequently.'
    )
    st.pyplot(fig)


def analysis_distance_from_work_level(data: pd.DataFrame,
                                      visits: pd.DataFrame) -> None:
    """
    This function plots the analysis at distance from work level.
    Args:
        data (pd.DataFrame): Dataframe with the data.
        visits (pd.DataFrame): Dataframe with the visits.
    Returns:
        Analysis at distance from work level.
    """
    st.header('Analysis at distance from work level')
    st.subheader(
        'Total estimated visits and customers per Planet Fitness location per distance from work'
    )

    # Grouping data
    grouped_visits = visits.groupby(['place',
                                     'distance_from_work_miles']).agg({
                                         'visit_weight':
                                         'sum'
                                     }).reset_index()
    grouped_customers = data.groupby(
        ['device_id', 'place', 'distance_from_work_miles']).agg({
            'customer_weight':
            'sum'
        }).reset_index()

    # Plotting
    fig, ax = plt.subplots(2, 1, figsize=(50, 10))
    sns.kdeplot(data=grouped_visits,
                x='distance_from_work_miles',
                hue='place',
                fill=True,
                ax=ax[0])
    sns.kdeplot(data=grouped_customers,
                x='distance_from_work_miles',
                hue='place',
                fill=True,
                ax=ax[1])
    ax[0].set_title('Distribution of distance from work for visits')
    ax[1].set_title('Distribution of distance from work for customers')

    # Show the plot in Streamlit
    st.write(
        'These KDE plots show the distribution of distance from work for each gym.'
        +
        ' Similarly, we can see that the total estimated visits and customers of alpharetta is lower than the other venues for all distances from work.'
        +
        ' The conclusion drawn from the data is that the distribution of customers distance from work to the different Planet Fitness locations is more evenly spread out compared to the distribution of visits. The graph indicates that customers are willing to travel greater distances from work to visit a Planet Fitness gym, but the frequency of visits decreases as the distance from work to the gym increases (as expected).'
        +
        ' Furthermore, the graph reveals an interesting observation about the Molly Planet Fitness location. It shows a large number of visits for a distance greater than 20 miles from work, which suggests that the gym is likely located in a residential area. This observation is important as it can help Planet Fitness to better understand the demographics of their customers and their behavior in terms of traveling to the gym.'
    )
    st.pyplot(fig)


#! GEO-LOCATION ANALYSIS
def map_venue(customers: pd.DataFrame, customers_venue: pd.DataFrame,
              color: str) -> None:
    """
    This function plots the map of Alpharetta.
    Args:
        data (pd.DataFrame): Dataframe with the data.
    Returns:
        Map of Alpharetta.
    """
    m = folium.Map(
        location=[
            customers['venue_lat'].mean(),
            customers['venue_long'].mean(),
        ],
        zoom_start=10,
        tiles='openstreetmap',
    )

    # Venue
    for _, row in customers_venue.iterrows():
        folium.CircleMarker(
            [row['venue_lat'], row['venue_long']],
            radius=20,
            fill_color='black',
        ).add_to(m)

        folium.CircleMarker(
            [row['user_home_lat'], row['user_home_long']],
            radius=10,
            fill_color=color,
        ).add_to(m)

        folium.PolyLine([[row['user_home_lat'], row['user_home_long']],
                         [row['user_work_lat'], row['user_work_long']]],
                        color=color).add_to(m)

    # Display the map
    m