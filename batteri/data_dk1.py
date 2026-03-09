# import os
# import matplotlib
# #print(matplotlib.get_backend())
# matplotlib.use('Qt5Agg')  # Use a non-interactive backend for matplotlib
# #print(matplotlib.get_backend())
# from matplotlib import pyplot as plt
# import requests
# import pandas as pd
# import statsmodels.api as sm

#fcr_dk1
# base_url = "https://api.energidataservice.dk/dataset/FcrDK1"
# params = {
#     'offset': 0,
#     'start': '2025-01-01T00:00',
#     'end': '2026-01-01T00:00',
#     'sort': 'HourUTC DESC'
# }
# hent_data = requests.get(base_url, params=params)
# data = hent_data.json()
# fcr_dk1 = pd.DataFrame(data['records'], columns=["HourDK", "FCRdk_DKK"])
# fcr_dk1["HourDK"] = pd.to_datetime(fcr_dk1["HourDK"])
# fcr_dk1 = fcr_dk1.set_index("HourDK").resample('4h').mean().reset_index()
# fcr_dk1["change"] = fcr_dk1["FCRdk_DKK"].diff()

# #day_ahead before october 1
# base_url = "https://api.energidataservice.dk/dataset/Elspotprices"
# params = {
#     'offset': 0,
#     'start': '2025-01-01T00:00',
#     'end': '2025-09-30T00:00',
#     'filter': '{"PriceArea":["DK1"]}',
#     'sort': 'HourUTC DESC'}

# day_ahead_response = requests.get(base_url, params=params)


# day_ahead_data = day_ahead_response.json()
# day_ahead_df_before_october = pd.DataFrame(day_ahead_data['records'], columns=["HourDK", "SpotPriceDKK"])

# day_ahead_df_before_october = day_ahead_df_before_october.rename(columns={"SpotPriceDKK": "PrisDKK", "HourDK": "DateTime"})

# day_ahead_df_before_october["DateTime"] = pd.to_datetime(day_ahead_df_before_october["DateTime"])
# day_ahead_df_before_october = day_ahead_df_before_october.set_index("DateTime").resample('4h').mean().reset_index()
   
# day_ahead_df_before_october["change"] = day_ahead_df_before_october["PrisDKK"].diff()

# #day_ahead after october 1
# base_url = "https://api.energidataservice.dk/dataset/DayAheadPrices"
# params = {
#     'offset': 0,
#     'start': '2025-10-01T00:00',
#     'end': '2026-01-01T00:00',
#     'filter': '{"PriceArea":["DK1"]}'
# }
# dayahead_response = requests.get(base_url, params=params)
# dayahead_data = dayahead_response.json()
# dayahead_df_after_october = pd.DataFrame(dayahead_data['records'], columns=["TimeDK", "DayAheadPriceDKK"])
# dayahead_df_after_october = dayahead_df_after_october.rename(columns={"DayAheadPriceDKK": "PrisDKK", "TimeDK": "DateTime"})
# dayahead_df_after_october["DateTime"] = pd.to_datetime(dayahead_df_after_october["DateTime"])
# dayahead_df_after_october = dayahead_df_after_october.set_index("DateTime").resample('4h').mean().reset_index()
# dayahead_df_after_october["change"] = dayahead_df_after_october["PrisDKK"].diff()

# #append day_ahead before october 1 and day_ahead after october 1
# dayahead_df = pd.concat([day_ahead_df_before_october, dayahead_df_after_october], ignore_index=True)
# print(dayahead_df.head(-5))


# #Wind forecast
# base_url = "https://api.energidataservice.dk/dataset/Forecasts_Hour"
# params = {
#     'offset': 0,
#     'start': '2025-01-01T00:00',
#     'end': '2026-01-01T00:00',
#     'filter': '{"PriceArea":["DK1"],"ForecastType":["Onshore Wind"]}',
#     'sort': 'HourUTC DESC'
# }
# wind_forecast_response = requests.get(base_url, params=params)
# wind_forecast_data = wind_forecast_response.json()

# wind_forecast_df = pd.DataFrame(wind_forecast_data['records'], columns=["HourDK", "ForecastDayAhead"])

# wind_forecast_df["HourDK"] = pd.to_datetime(wind_forecast_df["HourDK"])
# wind_forecast_df = wind_forecast_df.set_index("HourDK").resample('4h').mean().reset_index()
# wind_forecast_df["change"] = wind_forecast_df["ForecastDayAhead"].diff()


# #Solar forecast
# base_url = "https://api.energidataservice.dk/dataset/Forecasts_Hour"
# params = {
#     'offset': 0,
#     'start': '2025-01-01T00:00',
#     'end': '2026-01-01T00:00',
#     'filter': '{"PriceArea":["DK1"],"ForecastType":["Solar"]}',
#     'sort': 'HourUTC DESC'
# }
# solar_forecast_response = requests.get(base_url, params=params)
# solar_forecast_data = solar_forecast_response.json()

# solar_forecast_df = pd.DataFrame(solar_forecast_data['records'], columns=["HourDK", "ForecastDayAhead"])

# solar_forecast_df["HourDK"] = pd.to_datetime(solar_forecast_df["HourDK"])
# solar_forecast_df = solar_forecast_df.set_index("HourDK").resample('4h').mean().reset_index()
# solar_forecast_df["change"] = solar_forecast_df["ForecastDayAhead"].diff()



# ###
# df_merged = pd.merge(fcr_dk1, dayahead_df, left_on='HourDK', right_on='DateTime', how='outer').merge(wind_forecast_df, left_on='HourDK', right_on='HourDK', how='outer').merge(solar_forecast_df, left_on='HourDK', right_on='HourDK', suffixes=('_wind', '_solar'), how='outer')

# df_merged["datetime"] = df_merged["HourDK"].combine_first(df_merged["DateTime"])

# df_merged = df_merged.drop(columns=["HourDK", "DateTime"]).set_index("datetime").sort_index()

# filtered_df = df_merged.dropna()


# # fig, ax = plt.subplots(2,2, figsize=(8,8))
# # ax[0,0].plot(filtered_df.index, filtered_df["FCRdk_DKK"])
# # ax[0,0].set_title("FCRdk_DKK over time")
# # ax[0,1].plot(filtered_df.index, filtered_df["PrisDKK"])
# # ax[0,1].set_title("Elpris over time")
# # ax[1,0].plot(filtered_df.index, filtered_df["ForecastDayAhead_solar"])
# # ax[1,0].set_title("ForecastDayAhead_solar over time")
# # ax[1,1].plot(filtered_df.index, filtered_df["ForecastDayAhead_wind"])
# # ax[1,1].set_title("ForecastDayAhead_wind over time")
# # plt.show()



# # regression on levels
# filtered_df["time_trend"] = (filtered_df.index - filtered_df.index[0]).total_seconds() / 3600 # convert time trend to hours
# filtered_df["is_noon"] = (filtered_df.index.hour == 12).astype(int)
# X = sm.add_constant(filtered_df[["PrisDKK", "time_trend", "ForecastDayAhead_solar", "ForecastDayAhead_wind", "is_noon"]]) # add constant for intercept
# model = sm.OLS(filtered_df["FCRdk_DKK"], X).fit()
# #print(model.summary())
# #print(filtered_df.drop(columns=["change_solar", "change_wind", "change_x", "change_y"]).corr())

# # regression on changes
# filtered_df = filtered_df.set_index("datetime").sort_index()
# filtered_df["time_trend"] = (filtered_df.index - filtered_df.index[0]).total_seconds() / 3600 # convert time trend to hours
# X = sm.add_constant(filtered_df[["change_x", "change_wind", "change_solar"]]) # add constant for intercept
# model = sm.OLS(filtered_df["change_y"], X).fit()
# #print(model.summary())
# #print(filtered_df[["change_solar", "change_wind", "change_x", "change_y"]].corr())

# # fig, ax = plt.subplots(2,2, figsize=(12,6))
# # ax[0,0].plot(filtered_df.index, filtered_df["change_x"])
# # ax[0,0].set_title("Change in elpris over time")
# # ax[0,1].plot(filtered_df.index, filtered_df["change_y"])
# # ax[0,1].set_title("Change in FCRdk_DKK over time")
# # ax[1,0].plot(filtered_df.index, filtered_df["change_solar"])
# # ax[1,0].set_title("Change in solar forecast over time")
# # ax[1,1].plot(filtered_df.index, filtered_df["change_wind"])
# # ax[1,1].set_title("Change in wind forecast over time")
# # plt.show()
