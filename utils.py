import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from typing import Tuple, List
from streamlit_folium import st_folium
from notebooks.custom_functions import (
    find_optimal_clusters,
    get_customer_types,
    get_customer_types,
)

#! Selecting things


def multi_select_venues(data: pd.DataFrame) -> None:
    """
    This function allows the user to select venues to plot.
    Args:
        data (pd.DataFrame): Dataframe with the data.
    Returns:
        None.
    """
    # Get the list of venues
    venues = data['place'].unique()
    venues.sort()

    # Create a single select widget to select venues
    selected_venues = st.multiselect(
        'Select venues to plot',
        venues,
        default=venues,
    )
    return selected_venues


def one_select_venue(data: pd.DataFrame) -> None:
    """
    This function allows the user to select a venue to plot.
    Args:
        data (pd.DataFrame): Dataframe with the data.
    Returns:
        None.
    """
    # Get the list of venues
    venues = data['place'].unique()
    venues.sort()

    # Create a single select widget to select venues
    selected_venue = st.selectbox(
        'Select venue to plot',
        venues,
        index=0,
    )
    return selected_venue


# def display_venue_filters(data: pd.DataFrame) -> Tuple[str, str]:
#     """
#     This function displays the venue filters in the sidebar.
#     Args:
#         data (pd.DataFrame): Dataframe with the data.
#     Returns:
#         Venue and color.
#     """
#     venue_list = data['place'].unique().tolist()
#     venue_list.sort()
#     venue = st.sidebar.selectbox('Select Venue:', venue_list)
#     color_map = {
#         'alpharetta': 'blue',
#         'highway': 'orange',
#         'holcomb': 'green',
#         'molly': 'red'
#     }
#     color = color_map.get(venue, 'black')
#     st.header(f'Venue: {venue}')
#     return venue, color


#! Analysis
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
    st.subheader('Analysis at date level')
    st.caption(
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
    st.pyplot(fig)

    show_last_analysis = st.button('Show analysis')
    if show_last_analysis:
        st.write(
            """These line plots show the total estimated visits and customers of each gym per date.  
            Here, we can identify the underperforming gym of Alpharetta in comparison to the other gyms.
        """)
    else:
        st.write('')


def analysis_hour_level(data: pd.DataFrame, visits: pd.DataFrame) -> None:
    """
    This function plots the analysis at hour level.
    Args:
        data (pd.DataFrame): Dataframe with the data.
        visits (pd.DataFrame): Dataframe with the visits.
    Returns:
        Analysis at hour level.
    """
    st.subheader('Analysis at hour level')
    st.caption(
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
    st.pyplot(fig)

    show_last_analysis = st.button('Show analysis')
    if show_last_analysis:
        st.write(
            """These line plots show the average estimated visits and customers of each gym per hour.  
            Here, we can see that the total estimated visits and customers of alpharetta is lower than the other gyms in all periods of the day. Alpharetta only performs well in comparison to the other gyms at middays and at 19 h.
        """)
    else:
        st.write('')


def analysis_day_week_level(data: pd.DataFrame, visits: pd.DataFrame) -> None:
    """
    This function plots the analysis at day week level.
    Args:
        data (pd.DataFrame): Dataframe with the data.
        visits (pd.DataFrame): Dataframe with the visits.
    Returns:
        Analysis at day week level.
    """
    st.subheader('Analysis at day of week level')
    st.caption(
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
    st.pyplot(fig)

    show_last_analysis = st.button('Show analysis')
    if show_last_analysis:
        st.write(
            """These line plots show the average estimated visits of each gym per week day.  
            Here, we can see that the total estimated visits and customers of alpharetta is lower than the other gyms for all days of the week.
        """)
    else:
        st.write('')


def analysis_weekend_level(data: pd.DataFrame, visits: pd.DataFrame) -> None:
    """
    This function plots the analysis at weekend level.
    Args:
        data (pd.DataFrame): Dataframe with the data.
        visits (pd.DataFrame): Dataframe with the visits.
    Returns:
        Analysis at weekend level.
    """
    st.subheader('Analysis at weekend level')
    st.caption(
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
    st.pyplot(fig)

    show_last_analysis = st.button('Show analysis')
    if show_last_analysis:
        st.write(
            """These bar plots show the average estimated visits of each gym per weekend.  
            Here, we can see that the total estimated visits and customers of alpharetta is lower than the other venues for week days and weekends.  
            There is only one exception, which is the total estimated customers and visits of alpharetta at weekdays in comparison to higways.
        """)
    else:
        st.write('')


def analysis_month_level(data: pd.DataFrame, visits: pd.DataFrame) -> None:
    """
    This function plots the analysis at month level.
    Args:
        data (pd.DataFrame): Dataframe with the data.
        visits (pd.DataFrame): Dataframe with the visits.
    Returns:
        Analysis at month level.
    """
    st.subheader('Analysis at month level')
    st.caption(
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
    st.pyplot(fig)

    show_last_analysis = st.button('Show analysis')
    if show_last_analysis:
        st.write(
            """These line plots show the average estimated visits of each gym per month.  
            We can see that the total estimated visits and customers of alpharetta is lower than the other venues for all months of the year.  
            There is only one month in which Alpharetta performs decently in comparison to the other venues, and that is in the month of September.
        """)
    else:
        st.write('')


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
    st.subheader('Analysis at distance from home level')
    st.caption(
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
    st.pyplot(fig)

    show_last_analysis = st.button('Show analysis')
    if show_last_analysis:
        st.write(
            """These KDE plots show the distribution of distance from home for each gym.  
            We can see that the total estimated visits and customers of alpharetta is lower than the other venues for all distances from home.  
            The conclusion drawn from the data is that the distribution of customers distance from home to Planet Fitness in Alpharetta is more evenly spread out compared to the distribution of visits. The distribution of visits shows a significant increase for those who live closer to Planet Fitness in Alpharetta, indicating that customers who live in closer proximity to Planet Fitness in in Alpharetta are more likely to attend the gym frequently compared to those who live farther away.  
            This observation is interesting because it suggests that proximity to the gym is a significant factor in the frequency of visits by customers. People who live close to the gym may find it more convenient to attend the gym regularly, while those who live farther away may face more obstacles, such as transportation issues (?), that limit their ability to visit frequently.  
            Overall, this insight can be valuable for Planet Fitness as it can help them optimize their marketing efforts and target potential customers who live in the nearby areas. Additionally, the gym can also consider offering transportation or other incentives to customers who live farther away (free parking?, more parking cells?) to encourage them to visit more frequently.
            """)
    else:
        st.write('')


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
    st.subheader('Analysis at distance from work level')
    st.caption(
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
    st.pyplot(fig)

    show_last_analysis = st.button('Show analysis')
    if show_last_analysis:
        st.write(
            """These KDE plots show the distribution of distance from work for each gym.  
            Similarly, we can see that the total estimated visits and customers of alpharetta is lower than the other venues for all distances from work.  
            The conclusion drawn from the data is that the distribution of customers distance from work to the different Planet Fitness locations is more evenly spread out compared to the distribution of visits. The graph indicates that customers are willing to travel greater distances from work to visit a Planet Fitness gym, but the frequency of visits decreases as the distance from work to the gym increases (as expected).  
            Furthermore, the graph reveals an interesting observation about the Molly Planet Fitness location. It shows a large number of visits for a distance greater than 20 miles from work, which suggests that the gym is likely located in a residential area. This observation is important as it can help Planet Fitness to better understand the demographics of their customers and their behavior in terms of traveling to the gym.
            """)
    else:
        st.write('')


#! GEO-LOCATION ANALYSIS
# def location_venues(data: pd.DataFrame, color_underperforming: str,
#                     color_wellperforming: str) -> None:
#     """
#     This function plots the location of the venues.
#     Args:
#         data (pd.DataFrame): Dataframe with the data.
#         color_underperforming (str): Color for underperforming venues.
#         color_wellperforming (str): Color for wellperforming venues.
#     Returns:
#         Location of the venues.
#     """
#         m = folium.Map(
#         location=[data['venue_lat'].mean(), data['venue_long'].mean()],
#         zoom_start=14,
#         tiles='openstreetmap')

#     # Add a different color to place = 'alpharetta'
#     for i, place in enumerate(data['place'].unique()):
#         if place == 'alpharetta':
#             color = color_underperforming
#         else:
#             color = color_wellperforming
#         data_place = data[data['place'] == place]

#         # Add a marker for each place
#         folium.Marker(
#             location=[
#                 data_place['venue_lat'].mean(),
#                 data_place['venue_long'].mean()
#             ],
#             popup=place,
#             icon=folium.Icon(color=color, icon='info-sign'),
#         ).add_to(m)

#         # Including a legend for Alpharetta
#         legend_html = '''
#         <div style='position: fixed;
#                     bottom: 50px; left: 50px; width: 150px; height: 70px;
#                     border:2px solid grey; z-index:9999; font-size:14px;
#                     '>&nbsp; Underperforming &nbsp; <i class='fa fa-map-marker fa-2x' style='color:red'></i><br>
#                     &nbsp; Well_performing &nbsp; <i class='fa fa-map-marker fa-2x' style='color:blue'></i>
#         </div>
#         '''
#         m.get_root().html.add_child(folium.Element(legend_html))

#     # Display the map with the necessary zoom
#     m.fit_bounds(m.get_bounds())
#     st_folium(m, width=700, height=450)

# def map_venue(customers: pd.DataFrame, venue: str, color: str) -> None:
#     """
#     This function plots the map of Alpharetta.
#     Args:
#         data (pd.DataFrame): Dataframe with the data.
#     Returns:
#         Map of Alpharetta.
#     """
#     st.subheader('Geospatial analysis per Planet Fitness location')
#     st.caption(
#         'Origin of customers per Planet Fitness location (based on home location), and trip to work'
#     )

#     # Selecting customers data
#     customers_venue = customers[customers['place'] == venue]

#     m = folium.Map(
#         location=[
#             customers['venue_lat'].mean(),
#             customers['venue_long'].mean(),
#         ],
#         zoom_start=10,
#         tiles='openstreetmap',
#     )

#     # Venue
#     for _, row in customers_venue.iterrows():
#         folium.CircleMarker(
#             [row['venue_lat'], row['venue_long']],
#             radius=20,
#             fill_color='black',
#         ).add_to(m)

#         folium.CircleMarker(
#             [row['user_home_lat'], row['user_home_long']],
#             radius=10,
#             fill_color=color,
#         ).add_to(m)

#         folium.PolyLine([[row['user_home_lat'], row['user_home_long']],
#                          [row['user_work_lat'], row['user_work_long']]],
#                         color=color).add_to(m)

#     # Display the map
#     st_folium(m, width=700, height=450)


def map_venues(data: pd.DataFrame,
               customers: pd.DataFrame,
               selected_venues: List[str] = []) -> None:
    """
    This function plots the map of all venues.
    Args:
        data (pd.DataFrame): Dataframe with the data.
        customers (pd.DataFrame): Dataframe with the customers data.
        selected_venues (List[str]): List of selected venues to plot. If empty, all venues will be plotted.
    Returns:
        Map of selected venues.
    """
    st.subheader('Geospatial analysis per Planet Fitness location')
    st.caption(
        'Location of Planet Fitness gyms, and origin of customers per Planet Fitness location (based on home location), and trip to work'
    )
    # Create a dictionary of colors for each venue
    color_dict = {
        'alpharetta': 'blue',
        'highway': 'orange',
        'holcomb': 'green',
        'molly': 'red'
    }

    # If no venues were selected, plot all of them
    if not selected_venues:
        selected_venues = data['place'].unique()

    m = folium.Map(
        location=[
            customers['venue_lat'].mean(),
            customers['venue_long'].mean(),
        ],
        zoom_start=10,
        tiles='openstreetmap',
    )

    # Plot the selected venues
    for place in selected_venues:
        color = color_dict.get(place, 'black')

        # Plot the customers and their routes for the selected venue
        for _, row in customers[customers['place'] == place].iterrows():
            folium.CircleMarker(
                [row['user_home_lat'], row['user_home_long']],
                radius=10,
                fill_color=color,
            ).add_to(m)

            folium.PolyLine([[row['user_home_lat'], row['user_home_long']],
                             [row['user_work_lat'], row['user_work_long']]],
                            color=color).add_to(m)

        # Plot the venue location for the selected venue
        data_place = data[data['place'] == place]
        folium.Marker(
            location=[
                data_place['venue_lat'].mean(),
                data_place['venue_long'].mean()
            ],
            popup=place,
            icon=folium.Icon(color=color, icon='info-sign'),
        ).add_to(m)

    # Display the map
    st_folium(m, width=700, height=450)

    show_last_analysis = st.button('Show analysis')
    if show_last_analysis:
        st.write(
            """In the previous maps, we can see that Holcomb and Alpharetta are located in the same area.  
            This could suggest that the customers of Holcomb and Alpharetta are similar in terms of their distance from home and work. Therefore, one possible explanation of the underperformance of Alpharetta is that the customers of Alpharetta are similar to the customers of Holcomb. This could explain why the total estimated visits and customers of Alpharetta is lower than the other venues.
        """)
    else:
        st.write('')


def cluster_analysis(customers: pd.DataFrame, selected_venue: str) -> None:
    """
    This function plots the map of all venues.
    Args:
        data (pd.DataFrame): Dataframe with the data.
        customers (pd.DataFrame): Dataframe with the customers data.
    Returns:
        Map of selected venues.
    """
    st.subheader('Clustering analysis')
    st.caption('Clustering analysis of the customers based on their behavior')

    # Selecting customers data
    customers = customers.drop(
        [
            'user_home_lat', 'user_home_long', 'user_work_lat',
            'user_work_long', 'venue_lat', 'venue_long'
        ],
        axis=1,
    )

    # Filtering per venue
    customers_behavior = customers[customers['place'] == selected_venue].drop(
        ['device_id', 'place'], axis=1).reset_index(drop=True)

    # Applying clustering algorithm
    fig = find_optimal_clusters(customers_behavior, 10, 0.002)
    st.pyplot(fig)

    number_clusters = {
        'alpharetta': 3,
        'highway': 4,
        'holcomb': 4,
        'molly': 2,
    }
    # Getting the customer types
    optimal_clusters = number_clusters.get(selected_venue)

    customers_types = get_customer_types(
        customers_behavior,
        optimal_clusters,
    )
    # Showing in streamlit
    st.write(customers_types)

    show_last_analysis = st.button('Show analysis')
    if show_last_analysis:
        if selected_venue == 'alpharetta':
            st.write(
                """Based on the values of their features, the customer types can be labeled as follows:  
                ---  
                **Customer type 1:** These customers have a short distance from home and a moderate distance from work to the gym, spend a moderate amount of time in the gym, and visit during the afternoons. They tend to visit other nearby gyms some times, have a slight preference for visiting on weekends, and they go too often to the gym. **The 3.2% of the customers of alpharetta belong to this type and their customer weight is low**.  
                **Customer type 2:** These customers have a moderate distance from both home and work to the gym, spend a moderate amount of time in the gym, and visit during the afternoons. They tend to visit other nearby gyms, have a slight preference for visiting on weekends, and they rarely go to the gym. **The 96.5% of the customers of alpharetta belong to this type and their customer weight is too low**.  
                **Customer type 3:** These customers have a long distance from home and a short distance from work to the gym, spend more time in the gym, and visit the gym at night. They **do not** tend to visit other nearby gyms, **do not** tend to visit the gyms on weekends and they go too often to the gym. **Only the 0.2% of the customers of alpharetta belong to this type and their customer weight is very high**.  
            """)
        elif selected_venue == 'highway':
            st.write(
                """Based on the values of their features, the customer types can be labeled as follows:  
                ---  
                **Customer type 1:** These customers have a moderate distance from both home and work to the gym, spend a moderate amount of time in the gym, and visit during the first hours of the afternoon. They **do not** tend to visit other nearby gyms and have a **high** preference for visiting on weekends and they do not go too often to the gym. **The 91.6% of the customers of highway belong to this type and their customer weight is too low**.  
                **Customer type 2:** These customers have a moderate distance from both home and work to the gym, spend a high amount of time in the gym, and visit during the first hours of the afternoon. They tend to visit other nearby gyms, have a slight preference for visiting on weekends and they moderately often go to the gym. **The 2.5% of the customers of highway belong to this type and their customer weight is low-moderate**.  
                **Customer type 3:** These customers have a moderate distance from both home and work to the gym, spend a high amount of time in the gym, and visit during the first hours of the afternoon. They do not tend to visit other nearby gyms, they do not visit the gym on weekends and they moderately often go to the gym. **The 0.9% of the customers of highway belong to this type and their customer weight is low-moderate**.  
                **Customer type 4:** These customers have a moderate distance from home and a long distance from work to the gym, spend a high amount of time in the gym, and visit during the first hours of the afternoon. They do not tend to visit other nearby gyms, have a slight preference for visiting on weekends and they do not go too often to the gym. **The 4.9% of the customers of highway belong to this type and their customer weight is low**.
            """)
        elif selected_venue == 'holcomb':
            st.write(
                """Based on the values of their features, the customer types can be labeled as follows:  
                ---  
                **Customer type 1:** These customers have a moderate distance from both home and work to the gym, spend a high amount of time in the gym, and visit during the afternoons. They **do not** tend to visit other nearby gyms, have a **high** preference for visiting on weekends and they do not go too often to the gym. **The 84.3% of the customers of holcomb belong to this type and their customer weight is too low**.  
                **Customer type 2:** These customers have a short distance from home and a moderate distance from work to the gym, spend a moderate amount of time in the gym, and visit during the mornings. They **do not** tend to visit other nearby gyms, have a slight preference for visiting on weekends and they often go to the gym. **The 0.5% of the customers of holcom belong to this type and their customer weight is moderate**.  
                **Customer type 3:** These customers have a short distance from home and a moderate distance from work to the gym, spend a high amount of time in the gym, and visit during the afternoons. They **do not** tend to visit other nearby gyms, have a slight preference for visiting on weekends and they ocasionally go to the gym. **The 1.9% of the customers of holcom belong to this type and their customer weight is low-moderate**.  
                **Customer type 4:** These customers have a moderate distance from both home and work to the gym, spend a high amount of time in the gym, and visit during the afternoons. They **do not** tend to visit other nearby gyms, have a **high** preference for visiting on weekends and they do not go too often to the gym. **The 13.4% of the customers of holcom belong to this type and their customer weight is low-moderate**.
            """)
        elif selected_venue == 'molly':
            st.write(
                """Based on the values of their features, the customer types can be labeled as follows:  
                ---  
                **Customer type 1:** These customers have a moderate distance from both home and work to the gym, spend a moderate amount of time in the gym, and visit during the afternoons. They do not tend to visit other nearby gyms, they tend to visit the gym on weekends and they do not go too often to the gym. **The 94.3% of the customers of alpharetta belong to this type and their customer weight is too low**.  
                **Customer type 2:** These customers have a short distance from home and a moderate distance from work to the gym, spend a moderate amount of time in the gym, and visit during the afternoons. They do not tend to visit other nearby gyms, have a slight preference for visiting on weekends and they moderately often go to the gym. **The 5.7% of the customers of alpharetta belong to this type and their customer weight is low-moderate**.
            """)
    else:
        st.write('')
