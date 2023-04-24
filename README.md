# The People Platform - DS Challenge

![badge1](https://img.shields.io/badge/language-Python-blue.svg)
![badge2](https://img.shields.io/badge/framework-Streamlit-brightgreen.svg)

## General

This repository is associated with the Challenge described in this [link](https://github.com/jdpinedaj/tpp/tree/master/document).
This challenge is about analyzing why is a Planet Fitness location not performing as well as other locations.

## Files

- `notebooks/exploration.ipynb` holds the exploratory analysis in a Jupyter Notebook.
- `notebooks/custom_functions.py` contains the functions used in the notebook.
- `output/data.csv` is the output of the data after the cleaning and feature engineering processes.
- `output/customers.csv` is the output of the customers data after the cleaning and feature engineering processes, filtering by customers.
- `dashboard.py` is the script to run the dashboard using Streamlit.
- `utils.py` contains the functions used in the dashboard.
- `requirements.txt` contains the dependencies.
- `data` folder contains the data used in the challenge.

## How to run the dashboard

In order to run the dashboard, you need to have Python 3.7 or higher installed.\
Then, you need to install the dependencies using the following command:

`pip install -r requirements.txt`

Finally, you can run the dashboard using the following command:

`streamlit run dashboard.py`

## How to access the dashboard using Streamlit Sharing

You can access the dashboard using Streamlit Sharing using the following link:

[https://jdpinedaj-tpp-dashboard-5s2sci.streamlit.app/](https://jdpinedaj-tpp-dashboard-5s2sci.streamlit.app/)

## Conclusions

#### What did I receive?

I received a dataset with information about the customers of four Planet Fitness locations. The datasets are in CSV format and contain the following information:

- `device_id`: Unique identifier for each customer.
- `visit_id`: Unique identifier for each visit to each Planet Fitness location.
- `visit_start_time`: Timestamp of the start of the visit.
- `visit_end_time`: Timestamp of the end of the visit.
- `visit_lat` and `visit_long`: Latitude and longitude of the visit.
- `visit_weight`: Weight of the visit.
- `customer_weight`: Weight of the customer.
- `user_home_lat` and `user_home_long`: Latitude and longitude of the customer's home.
- `user_work_lat` and `user_work_long`: Latitude and longitude of the customer's work.

In addition, I received a dataset with information about the four Planet Fitness locations. The dataset is in CSV format and contains the following information:

- `venue_name`: Type of the venue. In this case, it is always Planet Fitness.
- `venue_address`: Address of the Planet Fitness location.
- `venue_lat` and `venue_long`: Latitude and longitude of the Planet Fitness location.
- `notes`: Notes about the Planet Fitness location. It says whether the location is underperforming or not.

#### What did I do?

I started by merging the datasets and then applying some feature engineering processes with the aim of creating additional features that could be useful for the analysis, such as:

- `start_date`: Date of the visit.
- `time_in_place_minutes`: Time in place in minutes.
- `day_of_week`: Day of the week of the visit.
- `weekend`: Whether the visit was on a weekend or not.
- `month`: Month of the visit.
- `visit_hour`: Hour of the visit.
- `distance_from_home_miles`: Distance from home in miles. It was calculated using the haversine formula.
- `distance_from_work_miles`: Distance from work in miles. It was calculated using the haversine formula.

Then, I performed some data cleaning processes with the aim of removing outliers in some features, such as `time_in_place_minutes`, `distance_from_home_miles`, and `distance_from_work_miles`, using the Interquartile Range method.

Subsequently, I performed some exploratory analysis to answer the questions in the challenge, by using the following techniques:

- Univariate analysis: I used histograms, lineplots, and barplots to analyze the distribution of the data.
- Geo-location analysis: I used the `folium` library to plot the home and work locations of the customers in a map, and their relationship with each Planet Fitness location.
- Clustering analysis: I used the `KMeans` algorithm to cluster the customers of each Planet Fitness location, with the aim of finding out the customer types of each location.

Finally, I created a dashboard using the `Streamlit` library to visualize the results of the analysis.

#### What did I find out?

##### Date, hours, days of the week, weekends, and months

From the univariate analysis, we can see that the total estimated visits of Alpharetta gym is lower than the other nearby gyms, suggesting that Alpharetta gym is underperforming in comparison to the other nearby gyms.

In terms of hours, we can see that the customers of Alpharetta gym tend to visit the gym at midday and in the night, while the customers of Holcomb gym (which is the closest gym to Alpharetta gym) tend to visit the gym in the morning and in the night. This could suggest that Alpharetta gym is not offering the right programs or services to attract and retain customers that prefer to visit the gym in the morning.

In terms of days of the week, we can see a similar trend for the customers of all four gyms for all days of the week, except for the customers of Holcomb gym on Fridays. This could suggest that customers that can choose between Holcomb and Alpharetta gyms tend to prefer Holcomb gym on Fridays, reducing the number of customers of Alpharetta gym on Fridays, which can cause Alpharetta gym to underperform in comparison to the other nearby gyms.

In terms of weekends, we see a similar behavior for the customers of all four gyms, except for the fact that the customers of Alpharetta gym tend to have a major preference for visiting on weekdays in comparison to customers of Highway gym. However, I can't draw any conclusions from this information, since the number of customers of Alpharetta gym is lower than the other nearby gyms.

In terms of months, we can see that the customers of Alpharetta gym underperform in comparison to the other nearby gyms in all months, except for the month of November, which is the month with lower number of estimated visits for all gyms. In addition, Holcomb gym (the closest gym to Alpharetta gym) overperforms in comparison to Alpharetta by a large margin between the months of March and June, probably taking many customers from Alpharetta gym.

##### Home and work locations

The distribution of customers' distance from home to Planet Fitness in Alpharetta is more evenly spread out compared to the distribution of visits. The distribution of visits shows a significant increase for those who live closer to Planet Fitness in Alpharetta, indicating that customers who live in closer proximity to Planet Fitness in in Alpharetta are more likely to attend the gym frequently in comparison to those who live farther away.

This observation is interesting because it suggests that **proximity to the gym** is a significant factor in the frequency of visits by customers. People who live close to the gym may find it more convenient to attend the gym regularly, while those who live farther away may face more obstacles, such as transportation issues (?), that limit their ability to visit frequently.

Overall, this insight can be valuable for Planet Fitness as it can help them optimize their marketing efforts and target potential customers who live in the nearby areas. Additionally, the gym can also consider offering transportation or other incentives to customers who live farther away (free parking?, more parking cells?) to encourage them to visit more frequently.

Similarly, the distribution of the distance from clients' workplaces to the various Planet Fitness locations is more dispersed than the distribution of visits. Customers are willing to travel further from work to visit a Planet Fitness gym, but the distance for visits is reduced (not spread as far over long distances), as would be expected.

In addition, the graphic reveals an intriguing observation about Molly's Planet Fitness's location. It reveals a high number of visits more than 20 miles from work (and the distance to home graph above revealed a large population with short commutes), implying that the gym is most likely located in a residential area. This observation is significant because it can help Planet Fitness better understand its customer demographics and behavior when it comes to gym visits.

##### Maps

From the maps, we can see that Holcomb and Alpharetta are located in the same area.

This could suggest that the customers of Holcomb and Alpharetta are similar in terms of their distance from home and work. Therefore, **one possible explanation of the underperformance of Alpharetta is that the customers of Alpharetta are similar to the customers of Holcomb**. This could explain why the total estimated visits and customers of Alpharetta is lower than the other venues.

##### Clustering

Based on the given information about the different types of customers for Alpharetta, Holcomb, and Highway, we can identify several factors that may contribute to Alpharetta gym's underperformance in comparison to the other two nearby gyms:

- **Customer preferences on weekends:** Alpharetta gym's customers tend to have a slight preference for visiting on weekends, while Holcomb gym's customers have a high preference for visiting on weekends. Highway gym's customers also have a high preference for visiting on weekends. This may suggest that Alpharetta gym is not offering the right programs or services to attract and retain customers that prefer to visit the gym on weekends.

- **Competition:** Alpharetta gym's customers tend to visit other nearby gyms some times, while Holcomb and Highway gyms' customers do not tend to visit other nearby gyms that much. It is important to note that only the four Planet Fitness gyms in the area are considered as nearby gyms, as there is no more information about other gyms in the area. This may indicate that Alpharetta gym faces stronger competition in the area, which could impact its ability to attract and retain customers.

Taken together, these factors suggest that the Alpharetta gym may need to adjust its approach to better meet the needs and preferences of its customers, and to better compete with nearby gyms.
This could involve changes to its offerings, pricing, marketing, or other factors that affect the customer experience.
