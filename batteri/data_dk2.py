import os
import matplotlib
from sklearn.model_selection import train_test_split
#print(matplotlib.get_backend())
matplotlib.use('Agg')  # Use a non-interactive backend for matplotlib
#print(matplotlib.get_backend())
from matplotlib import pyplot as plt
import requests
import pandas as pd
import statsmodels.api as sm
import base64
from io import BytesIO
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from smolagents import CodeAgent, InferenceClientModel, VisitWebpageTool


# fcr-d_ned
def hent_fcr_d_ned_data():    
    base_url = "https://api.energidataservice.dk/dataset/FcrNdDK2"
    params = {
        'offset': 0,
        'start': '2025-01-01T00:00',
        'end': '2026-01-01T00:00',
        'sort': 'HourUTC DESC',
        'filter': '{"PriceArea":["DK2"], "ProductName":["FCR-D ned"], "AuctionType":["Total"]}'
    }
    hent_data = requests.get(base_url, params=params)
    data = hent_data.json()
    df = pd.DataFrame(data['records'], columns=["HourDK", "PurchasedVolumeLocal", "PurchasedVolumeTotal", "PriceTotalEUR"])    
    df = df.rename(columns={"HourDK": "DateTime", "PurchasedVolumeLocal": "FCR-D_ned_PurchasedVolumeLocal", "PurchasedVolumeTotal": "FCR-D_ned_PurchasedVolumeTotal", "PriceTotalEUR": "FCR-D_ned_TotalPriceEUR"})
    df["DateTime"] = pd.to_datetime(df["DateTime"])
    df.to_excel("FCR-D_ned.xlsx", index=False)

# fcr-d_op
def hent_fcr_d_op_data():
    base_url = "https://api.energidataservice.dk/dataset/FcrNdDK2"
    params = {
        'offset': 0,
        'start': '2025-01-01T00:00',
        'end': '2026-01-01T00:00',
        'sort': 'HourUTC DESC',
        'filter': '{"PriceArea":["DK2"], "ProductName":["FCR-D upp"], "AuctionType":["Total"]}'
    }
    hent_data1 = requests.get(base_url, params=params)
    data1 = hent_data1.json()
    df1 = pd.DataFrame(data1['records'], columns=["HourDK", "PurchasedVolumeLocal", "PurchasedVolumeTotal", "PriceTotalEUR"])
    df1 = df1.rename(columns={"HourDK": "DateTime", "PurchasedVolumeLocal": "FCR-D_op_PurchasedVolumeLocal", "PurchasedVolumeTotal": "FCR-D_op_PurchasedVolumeTotal", "PriceTotalEUR": "FCR-D_op_TotalPriceEUR"})
    df1["DateTime"] = pd.to_datetime(df1["DateTime"])
    df1.to_excel("FCR-D_op.xlsx", index=False)

# fcr-n
def hent_fcr_n_data():
    base_url = "https://api.energidataservice.dk/dataset/FcrNdDK2"
    params = {
        'offset': 0,
        'start': '2025-01-01T00:00',
        'end': '2026-01-01T00:00',
        'sort': 'HourUTC DESC',
        'filter': '{"PriceArea":["DK2"], "ProductName":["FCR-N"], "AuctionType":["Total"]}'
    }
    hent_data2 = requests.get(base_url, params=params)
    data2 = hent_data2.json()
    df2 = pd.DataFrame(data2['records'], columns=["HourDK", "PurchasedVolumeLocal", "PurchasedVolumeTotal", "PriceTotalEUR"])
    df2 = df2.rename(columns={"HourDK": "DateTime", "PurchasedVolumeLocal": "FCR-N_PurchasedVolumeLocal", "PurchasedVolumeTotal": "FCR-N_PurchasedVolumeTotal", "PriceTotalEUR": "FCR-N_TotalPriceEUR"})
    df2["DateTime"] = pd.to_datetime(df2["DateTime"])
    df2.to_excel("FCR-N.xlsx", index=False)

# fig, ax = plt.subplots(figsize=(12, 6))
# df_fcr.set_index("DateTime", inplace=True)
# ax.plot(df_fcr.index, df_fcr["FCR-D_ned_TotalPriceEUR"], label="FCR-D ned TotalPriceEUR")
# ax.plot(df_fcr.index, df_fcr["FCR-D_op_TotalPriceEUR"], label="FCR-D op TotalPriceEUR")
# ax.plot(df_fcr.index, df_fcr["FCR-N_TotalPriceEUR"], label="FCR-N TotalPriceEUR")
# ax.set_xlabel("DateTime")
# ax.set_ylabel("Total Price EUR")
# ax.set_title("FCR Prices Over Time")
# ax.legend()
# df_fcr.reset_index(inplace=True)


#Wind forecast
def hent_wind_forecast_data():
    base_url = "https://api.energidataservice.dk/dataset/Forecasts_Hour"
    params = {
        'offset': 0,
        'start': '2025-01-01T00:00',
        'end': '2026-01-01T00:00',
        'filter': '{"PriceArea":["DK2"],"ForecastType":["Onshore Wind"]}',
        'sort': 'HourUTC DESC'
    }
    hent_data3 = requests.get(base_url, params=params)
    data3 = hent_data3.json()
    df3 = pd.DataFrame(data3['records'], columns=["HourDK", "ForecastDayAhead"])
    df3 = df3.rename(columns={"HourDK": "DateTime", "ForecastDayAhead": "ForecastDayAhead_wind"})
    df3["DateTime"] = pd.to_datetime(df3["DateTime"])
    df3.to_excel("Wind_forecast.xlsx", index=False)

#Solar forecast
def hent_solar_forecast_data():
    base_url = "https://api.energidataservice.dk/dataset/Forecasts_Hour"
    params = {
        'offset': 0,
        'start': '2025-01-01T00:00',
        'end': '2026-01-01T00:00',
        'filter': '{"PriceArea":["DK2"],"ForecastType":["Solar"]}',
        'sort': 'HourUTC DESC'
    }
    hent_data4 = requests.get(base_url, params=params)
    data4 = hent_data4.json()
    df4 = pd.DataFrame(data4['records'], columns=["HourDK", "ForecastDayAhead"])
    df4 = df4.rename(columns={"HourDK": "DateTime", "ForecastDayAhead": "ForecastDayAhead_solar"})
    df4["DateTime"] = pd.to_datetime(df4["DateTime"])
    df4.to_excel("Solar_forecast.xlsx", index=False)



#day ahead prices
#day_ahead before october 1
def hent_day_ahead_data():
    base_url = "https://api.energidataservice.dk/dataset/Elspotprices"
    params = {
        'offset': 0,
        'start': '2025-01-01T00:00',
        'end': '2025-09-30T00:00',
        'filter': '{"PriceArea":["DK2"]}',
        'sort': 'HourUTC DESC'}

    day_ahead_response = requests.get(base_url, params=params)
    day_ahead_data = day_ahead_response.json()
    day_ahead_df_before_october = pd.DataFrame(day_ahead_data['records'], columns=["HourDK", "SpotPriceDKK"])
    day_ahead_df_before_october = day_ahead_df_before_october.rename(columns={"SpotPriceDKK": "DayAheadPriceDKK", "HourDK": "DateTime"})
    day_ahead_df_before_october["DateTime"] = pd.to_datetime(day_ahead_df_before_october["DateTime"])
    day_ahead_df_before_october = day_ahead_df_before_october.set_index("DateTime").resample('1h').mean().reset_index()

    #day_ahead after october 1
    base_url = "https://api.energidataservice.dk/dataset/DayAheadPrices"
    params = {
        'offset': 0,
        'start': '2025-10-01T00:00',
        'end': '2026-01-01T00:00',
        'filter': '{"PriceArea":["DK2"]}'
    }
    dayahead_response = requests.get(base_url, params=params)
    dayahead_data = dayahead_response.json()
    dayahead_df_after_october = pd.DataFrame(dayahead_data['records'], columns=["TimeDK", "DayAheadPriceDKK"])
    dayahead_df_after_october = dayahead_df_after_october.rename(columns={"DayAheadPriceDKK": "DayAheadPriceDKK", "TimeDK": "DateTime"})
    dayahead_df_after_october["DateTime"] = pd.to_datetime(dayahead_df_after_october["DateTime"])
    dayahead_df_after_october = dayahead_df_after_october.set_index("DateTime").resample('1h').mean().reset_index()

    #append day_ahead before october 1 and day_ahead after october 1
    dayahead_df = pd.concat([day_ahead_df_before_october, dayahead_df_after_october], ignore_index=True)

    dayahead_df.to_excel("DayAheadPrices.xlsx", index=False)


df1 = pd.read_excel("FCR-D_ned.xlsx")
df2 = pd.read_excel("FCR-D_op.xlsx")
df3 = pd.read_excel("FCR-N.xlsx")
df4 = pd.read_excel("Wind_forecast.xlsx")
df5 = pd.read_excel("Solar_forecast.xlsx")
df6 = pd.read_excel("DayAheadPrices.xlsx")
df_fcr = pd.merge(df1, df2, on="DateTime", how="outer")
df_fcr = pd.merge(df_fcr, df3, on="DateTime", how="outer")
df_fcr = pd.merge(df_fcr, df4, on="DateTime", how="outer")
df_fcr = pd.merge(df_fcr, df5, on="DateTime", how="outer")
fcr_renew_dayahead = pd.merge(df_fcr, df6, on="DateTime", how="outer")




korrelation = fcr_renew_dayahead.drop(columns=["DateTime"]).corr()
fig, ax = plt.subplots(figsize=(10, 8))
cax = ax.imshow(korrelation, cmap='coolwarm', vmin=-1, vmax=1)
ax.set_xticks(range(len(korrelation.columns)))
ax.set_xticklabels(korrelation.columns, rotation=90)
ax.set_yticks(range(len(korrelation.columns)))
ax.set_yticklabels(korrelation.columns)
fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
ax.set_title("Correlation Matrix")
# i need more white space at bottom in order to see titles as they are quite long.
plt.subplots_adjust(bottom=0.4)



#prepare the following code for a html file through a view in django
annotation_right_corner_position = (pd.to_datetime('2025-12-31')+pd.Timedelta(days=15), 150-3)

def get_plots_for_prices():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3))
    variabler = ["FCR-D_ned_TotalPriceEUR", "FCR-D_op_TotalPriceEUR", "FCR-N_TotalPriceEUR"]
    for i, variabel in enumerate(variabler):
        # row = i // 4
        # col = i % 3
        axes[i].plot(fcr_renew_dayahead["DateTime"], fcr_renew_dayahead[variabel])
        axes[i].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b'))
        axes[i].set_ylim(0, 150)
        if variabel == "FCR-D_ned_TotalPriceEUR":
            axes[i].annotate('Ekstreme priser på 6-800 EUR/t', xy=(pd.to_datetime('2025-05-05'), 140), xytext=(pd.to_datetime('2025-05-30'), 140), ha='left', va='center', arrowprops=dict(facecolor='red', shrink=0.05), fontsize=7, color='red')
            axes[i].set_title("FCR_D nedregulering")
            axes[i].annotate('Et marked, som har stabiliseret \nsig siden 2023-24', xy=(pd.to_datetime('2025-12-31') + pd.Timedelta(days=15), 115), ha='right', va='center', fontsize=7, color='black',bbox=dict(boxstyle="round,pad=0.3", edgecolor='gray', facecolor='white', alpha=0.5))
        if variabel == "FCR-D_op_TotalPriceEUR":
            axes[i].annotate('De to FCR-D markeder mættes \nefterhånden med batterikapacitet \nsamt andre teknologier, som \ngodkendes til også at kunne \nlevere ydelsen', xy=annotation_right_corner_position, ha='right', va='top', fontsize=7, color='black',bbox=dict(boxstyle="round,pad=0.3", edgecolor='gray', facecolor='white', alpha=0.5))
            axes[i].set_title("FCR_D opregulering")
        if variabel == "FCR-N_TotalPriceEUR":
            axes[i].annotate('FCR-N er et mindre marked med et \nrelativt lille behov. Til gengæld \nrammer prisen sjældent nulpunktet', xy=annotation_right_corner_position, ha='right', va='top', fontsize=7, color='black',bbox=dict(boxstyle="round,pad=0.3", edgecolor='gray', facecolor='white', alpha=0.5))
            axes[i].set_title("FCR_N")
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)
    graf = base64.b64encode(image_png).decode('utf-8')
    return graf

def get_plot_for_daily_variation():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3))
    price_data = fcr_renew_dayahead[["DateTime", "FCR-D_ned_TotalPriceEUR", "FCR-D_op_TotalPriceEUR", "FCR-N_TotalPriceEUR"]]
    price_data.loc[price_data["FCR-D_ned_TotalPriceEUR"] > 100, "FCR-D_ned_TotalPriceEUR"] = 100
    price_data["Hour"] = price_data["DateTime"].dt.hour
    price_data["Month"] = price_data["DateTime"].dt.month
    price_data.drop(columns=["DateTime"], inplace=True)
    groupedprice_data = price_data.groupby(["Month","Hour"])[["FCR-D_ned_TotalPriceEUR", "FCR-D_op_TotalPriceEUR", "FCR-N_TotalPriceEUR"]].mean()
    #make a matrix visual with color grading. x-axis =hour, y-axis = month, color = price. make one for each of the three variables.
    variabler = ["FCR-D_ned_TotalPriceEUR", "FCR-D_op_TotalPriceEUR", "FCR-N_TotalPriceEUR"]
    for i, variabel in enumerate(variabler):
        pivot_table = groupedprice_data[variabel].unstack(level=0)
        cax = axes[i].imshow(pivot_table, aspect='auto', cmap='RdYlGn_r')
        axes[i].set_xticks(range(12))
        axes[i].set_yticks(range(24))
        axes[i].set_yticklabels(range(0, 24))
        #axes[i].set_xticklabels(range(1, 13))
        axes[i].set_xticklabels(['Jan', '', 'Mar', '', 'May', '', 'Jul', '', 'Sep', '', 'Nov', ''])
        #fig.colorbar(cax, ax=axes[i], fraction=0.046, pad=0.04)
        if variabel == "FCR-D_ned_TotalPriceEUR":
             axes[i].set_ylabel("Klokkeslæt")
             axes[i].set_title("FCR_D nedregulering")
        if variabel == "FCR-D_op_TotalPriceEUR":
             axes[i].set_title("FCR_D opregulering")
        if variabel == "FCR-N_TotalPriceEUR":
            axes[i].annotate('De højeste priser er typisk i \nmorgentimerne. Det vidner \nmåske om, at det er mere \nattraktivt at allokere sin enhed \ntil ren elsalg i disse timer', xy=(4.1, 8), xytext=(5, 8), arrowprops=dict(facecolor='red', shrink=0.05), fontsize=7, color='red')
            axes[i].set_title("FCR_N")
    
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)
    graf = base64.b64encode(image_png).decode('utf-8')
    return graf
    
def get_plots_for_purchasedvolumne():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3))
    variabler = ["FCR-D_ned_PurchasedVolumeLocal", "FCR-D_op_PurchasedVolumeLocal", "FCR-N_PurchasedVolumeLocal"]
    for i, variabel in enumerate(variabler):
        # row = i // 4
        # col = i % 3
        axes[i].plot(fcr_renew_dayahead["DateTime"], fcr_renew_dayahead[variabel])

        axes[i].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b'))
        axes[i].set_ylim(0, 150)
        if variabel == "FCR-D_ned_PurchasedVolumeLocal":
            axes[i].annotate('FCR-D handles på et fælles \ndansk-svensk marked. Det svenske \nmarked er langt større, og det er \ni høj grad de svenske aktører/marked \n(specielt vandkraft), som definerer prisen ', xy=annotation_right_corner_position, ha='right', va='top', fontsize=7, color='black',bbox=dict(boxstyle="round,pad=0.3", edgecolor='gray', facecolor='white', alpha=0.5))
            axes[i].set_title("FCR_D nedregulering")
        if variabel == "FCR-D_op_PurchasedVolumeLocal":
            axes[i].annotate('Energinets behov er på ca. 40-45 MW, \nsom i alle årets timer \nhar været dækket af danske aktører', xy=annotation_right_corner_position, ha='right', va='top', fontsize=7, color='black',bbox=dict(boxstyle="round,pad=0.3", edgecolor='gray', facecolor='white', alpha=0.5))
            axes[i].axhline(y=45, color='yellow', linestyle='--', linewidth=1)
            axes[i].set_title("FCR_D opregulering")
        if variabel == "FCR-N_PurchasedVolumeLocal":
            axes[i].annotate('Et mindre marked, hvor \nefterspørgslen kun er på 18 MW.', xy=annotation_right_corner_position, ha='right', va='top', fontsize=7, color='black',bbox=dict(boxstyle="round,pad=0.3", edgecolor='gray', facecolor='white', alpha=0.5))
            axes[i].axhline(y=18, color='yellow', linestyle='--', linewidth=1)
            axes[i].set_title("FCR_N")
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)
    graf = base64.b64encode(image_png).decode('utf-8')
    return graf

def get_plots_for_energy_prod():
    fig, axes = plt.subplots(1, 2, figsize=(12, 3))
    variabler = ["ForecastDayAhead_wind", "ForecastDayAhead_solar"]
    #make a new df with variables above and also resample to daily production by summin up hourly.
    fcr_renew_dayahead_daily = fcr_renew_dayahead.set_index("DateTime").resample("D")[variabler].sum().reset_index()
    for i, variabel in enumerate(variabler):
        # row = i // 4
        # col = i % 3
        axes[i].bar(fcr_renew_dayahead_daily["DateTime"], fcr_renew_dayahead_daily[variabel])
        axes[i].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b'))
        if variabel == "ForecastDayAhead_wind":
            axes[i].set_title("Vind på land")
        if variabel == "ForecastDayAhead_solar":
            axes[i].set_title("Sol")
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)
    graf = base64.b64encode(image_png).decode('utf-8')
    return graf

def get_plot_for_dayahead():
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(fcr_renew_dayahead["DateTime"], fcr_renew_dayahead["DayAheadPriceDKK"])
    ax.hlines(y=0, xmin=fcr_renew_dayahead["DateTime"].min(), xmax=fcr_renew_dayahead["DateTime"].max(), colors='gray', linestyles='--')
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b'))
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)
    graf = base64.b64encode(image_png).decode('utf-8')
    return graf

def correlation_matrix_outliers_removoed():
    data_copy = fcr_renew_dayahead.copy()
    for variabel in ["FCR-D_ned_TotalPriceEUR", "FCR-D_op_TotalPriceEUR"]:
        #mean_value = data_copy.loc[data_copy[variabel] <= 60, variabel].mean()
        data_copy.loc[data_copy[variabel] > 60, variabel] = 60
    
    korrelation = data_copy.drop(columns=["DateTime"]).corr()
    mask = np.triu(np.ones_like(korrelation, dtype=bool))
    fig, ax = plt.subplots(figsize=(10, 8))
    cax = ax.imshow(korrelation.mask(mask), cmap='coolwarm', vmin=-1, vmax=1)
    ax.set_xticks(range(len(korrelation.columns)))
    ax.set_xticklabels(korrelation.columns, rotation=90)
    ax.set_yticks(range(len(korrelation.columns)))
    ax.set_yticklabels(korrelation.columns)
    fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("Correlation Matrix")
    ax.annotate('Perioder med meget sol (sommer) og meget \nvind giver selvfølgelig lav elpris', xy=(9.5, 11), xytext=(9.5, 9), ha='center', va='center', fontsize=7, color='black',arrowprops=dict(facecolor='red', shrink=0.05))  
    ax.annotate('Når der købes FCR-D opregulering fra \ndanske aktører, købes der mindre \nFCR-N fra danske aktører, og omvendt', xy=(3, 7), xytext=(3, 5), ha='center', va='center', fontsize=7, color='black',arrowprops=dict(facecolor='red', shrink=0.05))
    ax.annotate('Høj pris på FCR-N -> Høj pris på FCR-D op, \nog omvendt. Måske følger priser for \nopregulering de samme mekanismer', xy=(5, 8), xytext=(9, 6.5), ha='center', va='center', fontsize=7, color='black',arrowprops=dict(facecolor='red', shrink=0.05))
    plt.subplots_adjust(bottom=0.4)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)
    graf = base64.b64encode(image_png).decode('utf-8')
    return graf

#create a scikit learn logistics regression model to predict FCR-D_op_TotalPriceEUR_class based on the two other variables. Print out the classification report and confusion matrix.
def logistic_regression_model():
    data_copy2 = fcr_renew_dayahead.copy()[["FCR-D_op_TotalPriceEUR", "ForecastDayAhead_solar", "ForecastDayAhead_wind"]].dropna()
    #classify FCR-D_op_TotalPriceEUR into two categories, high or low, sliced by the median value
    median_value = data_copy2["FCR-D_op_TotalPriceEUR"].median()
    data_copy2["FCR-D_op_TotalPriceEUR_class"] = data_copy2["FCR-D_op_TotalPriceEUR"].apply(lambda x: 1 if x > median_value else 0)
    X = data_copy2[["ForecastDayAhead_solar", "ForecastDayAhead_wind"]]
    y = data_copy2["FCR-D_op_TotalPriceEUR_class"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    classification_report_result = classification_report(y_test, y_pred)
    confusion_matrix_result = confusion_matrix(y_test, y_pred)
    accuracy_pct = round(classification_report(y_test, y_pred, output_dict=True)['accuracy'] * 100,1)
    print("Classification Report:\n", classification_report_result)
    print("Confusion Matrix:\n", confusion_matrix_result)
    print("Accuracy:\n", accuracy_pct)
    return accuracy_pct





###################### AGENTS, smolagents (codeagent)


#info = search_web(dk1_data)
#extracted_info = extract_information(info)
#extend ny data
#find min eller max på data fx

import requests
import pandas as pd
from smolagents import CodeAgent, InferenceClientModel

def FCR_AI_AGENT():
    agent = CodeAgent(tools=[], model=InferenceClientModel())
    base_url = "https://api.energidataservice.dk/dataset/FcrDK1"
    params = {
        "offset": 0,
        "start": "2025-01-01T00:00",
        "end": "2026-01-01T00:00",
        "sort": "HourUTC DESC",
        "limit": 1000
    }
    resp = requests.get(base_url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    df = pd.DataFrame(data["records"])
    fcr_dk1 = df[["HourDK", "FCRdk_DKK"]].copy()
    fcr_dk1["HourDK"] = pd.to_datetime(fcr_dk1["HourDK"])
    fcr_dk1 = fcr_dk1.sort_values("HourDK")
    # statistik (hurtigt og stabilt)
    avg = float(fcr_dk1["FCRdk_DKK"].mean())
    min_row = fcr_dk1.loc[fcr_dk1["FCRdk_DKK"].idxmin()]
    max_row = fcr_dk1.loc[fcr_dk1["FCRdk_DKK"].idxmax()]
    top_high = fcr_dk1.nlargest(5, "FCRdk_DKK")
    top_low  = fcr_dk1.nsmallest(5, "FCRdk_DKK")
    # lad agenten lave en kort forklaring baseret på opsummering (ikke 1000 rækker)
    summary_text = f"""
    Gennemsnit: {avg:.2f}
    Minimum: {min_row['FCRdk_DKK']:.2f} på {min_row['HourDK']}
    Maximum: {max_row['FCRdk_DKK']:.2f} på {max_row['HourDK']}
    Top 5 høje: {top_high.to_dict('records')}
    Top 5 lave: {top_low.to_dict('records')}
    Skriv en kort forklaring til en kunde: hvad er interessant og hvad betyder det?
    """
    insight = agent.run(summary_text)
    # returnér template-klar context
    return {
        "average": round(avg, 2),
        "min": {"value": float(min_row["FCRdk_DKK"]), "time": min_row["HourDK"].strftime("%Y-%m-%d %H:%M")},
        "max": {"value": float(max_row["FCRdk_DKK"]), "time": max_row["HourDK"].strftime("%Y-%m-%d %H:%M")},
        "top_high": [
            {"time": r["HourDK"].strftime("%Y-%m-%d %H:%M"), "value": float(r["FCRdk_DKK"])}
            for _, r in top_high.iterrows()
        ],
        "top_low": [
            {"time": r["HourDK"].strftime("%Y-%m-%d %H:%M"), "value": float(r["FCRdk_DKK"])}
            for _, r in top_low.iterrows()
        ],
        "insight": str(insight),
    }


def investerings_case():
   daily_data = fcr_renew_dayahead
   # for all prices above 100, set to 100.
   for variabel in ["FCR-D_ned_TotalPriceEUR", "FCR-D_op_TotalPriceEUR", "FCR-N_TotalPriceEUR"]:
        daily_data.loc[daily_data[variabel] > 80, variabel] = 80
   daily_data = fcr_renew_dayahead.set_index("DateTime").resample("4h")[["FCR-D_ned_TotalPriceEUR", "FCR-D_op_TotalPriceEUR", "FCR-N_TotalPriceEUR"]].mean().reset_index()
   daily_data["High_Price"] = daily_data[["FCR-D_ned_TotalPriceEUR", "FCR-D_op_TotalPriceEUR", "FCR-N_TotalPriceEUR"]].max(axis=1)
   daily_data["High_Price_pricetype"] = daily_data[["FCR-D_ned_TotalPriceEUR", "FCR-D_op_TotalPriceEUR", "FCR-N_TotalPriceEUR"]].idxmax(axis=1)
   average_price_for_all_high_prices = round((daily_data["High_Price"].mean())*7.45,2)
   print(daily_data.head())
   return {"average_price_for_all_high_prices": average_price_for_all_high_prices,
           "aarlig_indtjening": average_price_for_all_high_prices*24*365,
           "antal_4h_periode_på_respektive_markeder": daily_data["High_Price_pricetype"].value_counts().to_dict()}

