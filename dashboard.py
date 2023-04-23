import streamlit as st
import pandas as pd
from utils import (
    multi_select_venues,
    one_select_venue,
    # display_venue_filters,
    analysis_date_level,
    analysis_hour_level,
    analysis_day_week_level,
    analysis_weekend_level,
    analysis_month_level,
    analysis_distance_from_home_level,
    analysis_distance_from_work_level,
    # location_venues,
    # map_venue,
    map_venues,
    cluster_analysis,
)

APP_TITLE = 'Planet Fitness Customer Analysis'


def main():
    st.set_page_config(page_title=APP_TITLE,
                       layout='wide',
                       page_icon=':chart_with_upwards_trend:')
    st.image(image='images/tpp-logo.png', use_column_width=False, width=200)
    st.title(APP_TITLE)

    #! Load data
    # Reading the two datasets for plotting
    data = pd.read_csv('output/data.csv')
    visits = pd.read_csv('output/visits.csv')
    customers = pd.read_csv('output/customers.csv')

    # Selecting which analysis to show using buttons
    analysis = st.sidebar.radio(
        'Select analysis',
        [
            'Date',
            'Hour',
            'Day of Week',
            'Weekend',
            'Month',
            'Distance from Home',
            'Distance from Work',
            # 'Location of all venues', 'Geo-location one venue',
            'Geo-location all venues',
            'Clustering analysis',
        ])

    if analysis == 'Date':
        analysis_date_level(data, visits)
    elif analysis == 'Hour':
        analysis_hour_level(data, visits)
    elif analysis == 'Day of Week':
        analysis_day_week_level(data, visits)
    elif analysis == 'Weekend':
        analysis_weekend_level(data, visits)
    elif analysis == 'Month':
        analysis_month_level(data, visits)
    elif analysis == 'Distance from Home':
        analysis_distance_from_home_level(data, visits)
    elif analysis == 'Distance from Work':
        analysis_distance_from_work_level(data, visits)
    # elif analysis == 'Location of all venues':
    #     location_venues(data,
    #                     color_underperforming='red',
    #                     color_wellperforming='blue')
    # elif analysis == 'Geo-location one venue':
    #     venue, color = display_venue_filters(data)
    #     map_venue(customers, venue, color)
    elif analysis == 'Geo-location all venues':
        selected_venues = multi_select_venues(data)
        map_venues(data, customers, selected_venues)
    elif analysis == 'Clustering analysis':
        selected_venue = one_select_venue(data)
        cluster_analysis(customers, selected_venue)
    else:
        st.write('Please select an analysis')


if __name__ == '__main__':
    main()
