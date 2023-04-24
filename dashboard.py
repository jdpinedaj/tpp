import streamlit as st
import pandas as pd
from utils import (
    analysis_date_level,
    analysis_hour_level,
    analysis_day_week_level,
    analysis_weekend_level,
    analysis_month_level,
    analysis_distance_from_home_level,
    analysis_distance_from_work_level,
    map_venues,
    cluster_analysis,
    conclusions_pf,
)

APP_TITLE = 'Planet Fitness Customer Analysis'

#TODO: Ajustar todas las conclusiones, PILAS!


def main():
    st.set_page_config(page_title=APP_TITLE,
                       layout='wide',
                       page_icon=':chart_with_upwards_trend:')
    st.image(image='images/tpp-logo.png', use_column_width=False, width=200)
    st.title(APP_TITLE)
    st.set_option('deprecation.showPyplotGlobalUse', False)

    #! Load data
    # Reading the two datasets for plotting
    data = pd.read_csv('output/data.csv')
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
            'Geo-location all venues',
            'Clustering analysis',
            'Conclusions',
        ],
    )

    if analysis == 'Date':
        column = 'start_date'
        analysis_date_level(data, column)
    elif analysis == 'Hour':
        column = 'visit_hour'
        analysis_hour_level(data, column)
    elif analysis == 'Day of Week':
        column = 'day_of_week'
        analysis_day_week_level(data, column)
    elif analysis == 'Weekend':
        column = 'weekend'
        analysis_weekend_level(data, column)
    elif analysis == 'Month':
        column = 'month'
        analysis_month_level(data, column)
    elif analysis == 'Distance from Home':
        column = 'distance_from_home_miles'
        analysis_distance_from_home_level(data, column)
    elif analysis == 'Distance from Work':
        column = 'distance_from_work_miles'
        analysis_distance_from_work_level(data, column)
    elif analysis == 'Geo-location all venues':
        map_venues(data, customers)
    elif analysis == 'Clustering analysis':
        cluster_analysis(customers, data)
    elif analysis == 'Conclusions':
        conclusions_pf()
    else:
        st.write('Please select an analysis')


if __name__ == '__main__':
    main()
