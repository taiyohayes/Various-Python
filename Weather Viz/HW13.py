# Taiyo Hayes, tjhayes@usc.edu
# ITP 216, Fall 2022
# Section: 32081
# Homework 13
# Description: Visualization of Weather Data

import pandas as pd
import matplotlib.pyplot as plt


def main():
    # reading in the dataset
    df = pd.read_csv("weather.csv")

    # removing rows of data where the observed temp is null
    df = df[df["TOBS"].notnull()]

    # making a column for year: allows us to easily get the last 10 years
    df["YEAR"] = df["DATE"].str[0:4]
    years_list = list(df["YEAR"].unique())

    # making a column for month: allows us to group by month
    df["MONTH_DAY"] = df["DATE"].str[-5:]
    df = df[df['MONTH_DAY'] != '02-29']  # drop leap years
    month_days_list = list(df["MONTH_DAY"].unique())

    df.sort_values(inplace=True, by='MONTH_DAY')

    # list of months to label the x-axis of both graphs
    month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # list to help label x-axes
    x_list = list(range(0,365,31))

    # set up the figure
    fig, ax = plt.subplots(2, 1)
    fig.suptitle("LA Climatology Data (2018-2022)")

    # top graph
    ax[0].set_xticks(x_list, month_list)
    color_list = ["red", "blue", "green", "orange", "purple"]
    grouped_years = df.groupby("YEAR")
    i = 0
    for year in years_list:
        df_group = grouped_years.get_group(year)
        ax[0].plot(df_group["MONTH_DAY"], df_group["TOBS"], color=color_list[i],
                   label=year, linewidth=0.2)
        i += 1

    # bottom graph
    ax[1].set_xticks(x_list, month_list)
    df_2021 = df[df["YEAR"] == "2021"]
    df_hist = df[df["YEAR"] != "2021"]
    df_2021 = df_2021.drop_duplicates(subset="MONTH_DAY", keep="first")
    hist_list = []
    curr_list = list(df_2021["TOBS"])
    grouped_month_day = df_hist.groupby("MONTH_DAY")
    for date in month_days_list:
        df_group = grouped_month_day.get_group(date)
        hist_list.append(df_group["TOBS"].mean())
    ax[1].bar(month_days_list, hist_list, color="blue", label="historical average", linewidth=0.5)
    ax[1].bar(month_days_list, curr_list, color="orange", label="2021", linewidth=0.2)

    # output graphs with title, axis labels, and legend
    ax[0].set(title="Most recent 10 years", xlabel="Month", ylabel="temp (F)")
    ax[1].set(title="Comparing current year and historical averages",
              xlabel="Month", ylabel="temp (F)")
    ax[0].legend(loc=1, prop={'size':5})
    ax[1].legend(prop={'size':5})
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
