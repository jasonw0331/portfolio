import csv
import statistics
from functools import total_ordering

import matplotlib.pylab as plt
import seaborn as sns
from fontTools.subset.svg import xpath


def read_file(filename, date_index, field_index, has_header=True):
    """
    Reads a csv file and parses the content field into a time series.
    Input:
    filename: csv filename
    date_index: zero-based index of the time series date field
    field_index: zero-based index of the time series content field
    has_header: True or False on whether the file contents has a header row
    Output:
    time_series: list of tuples with tuple consisting of (date, content field)
    """
    time_series = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        if has_header:
            next(reader, None)
        for row in reader:
            time_series.append((row[date_index], float(row[field_index])))
    return time_series
def plot_rolling_statistics(ts_label, ts, window_size, ts_min, ts_max, ts_mean, ts_stdev,
                            is_bollinger_band=True):
    """ Plots the rolling statistics via a time series.

    Parameters:
    -----------
    ts_label: string
        time series label
    ts: list
        time series
    window_size: int
        window size
    ts_min: float
        time series of rolling min value
    ts_max: float
        time series of rolling max value
    ts_mean: float
        time series of rolling mean value
    ts_stdev: float
        time series of rolling standard deviation value

    """
    scale = 2 if is_bollinger_band else 1
    upper_bollinger_band_label = 'Mean + 2*Stdev' if is_bollinger_band else 'Mean + Stdev'
    lower_bollinger_band_label = 'Mean - 2*Stdev' if is_bollinger_band else 'Mean - Stdev'

    sns.set()
    fig, ax = plt.subplots()
    ax.plot([ts[i][0] for i in range(len(ts))], [ts[i][1] for i in range(len(ts))],
            linewidth=2, label=ts_label, color='black')
    ax.plot([ts_min[i][0] for i in range(len(ts_min))], [ts_min[i][1] for i in range(len(ts_min))],
            linewidth=1, label='Min', color='lightblue')
    ax.plot([ts_max[i][0] for i in range(len(ts_max))], [ts_max[i][1] for i in range(len(ts_max))],
            linewidth=1, label='Max', color='lightblue')
    ax.plot([ts_mean[i][0] for i in range(len(ts_mean))], [ts_mean[i][1] for i in range(len(ts_mean))],
            linewidth=1, label='Mean', color='red')
    ax.plot([ts_stdev[i][0] for i in range(len(ts_stdev))],
            [ts_mean[i][1] + scale * ts_stdev[i][1] for i in range(len(ts_stdev))],
            linewidth=1, label=upper_bollinger_band_label, color='orange')
    ax.plot([ts_stdev[i][0] for i in range(len(ts_stdev))],
            [ts_mean[i][1] - scale * ts_stdev[i][1] for i in range(len(ts_stdev))],
            linewidth=1, label=lower_bollinger_band_label, color='orange')
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title(f'{ts_label} with {window_size}-Day Rolling Statistics')
    ax.legend(loc='best', fontsize='x-small')
    plt.show()




def main():
    # read the data from the CSV file, copied the path from desktop (will need to change for each computer)
    try:
        ts = read_file('/Users/jasonwang/Desktop/Python Project 2/GOOG.csv', 0, 5, has_header=True)
    except FileNotFoundError:
        print("File not found. Please check the file path and try again.")
        exit()

    # user input for window size
    try:
        userinput_window_size = int(input('Enter window size: '))
        if userinput_window_size > len(ts):
            print('Invalid window size')
            return
        # empty list to store values within the loop
        ts_min_data = []
        ts_max_data = []
        ts_mean_data = []
        ts_stdev_data = []

        # calculate rolling statistics for each window
        for i in range(len(ts) - userinput_window_size + 1):
            window_data = ts[i:i + userinput_window_size]
            rolling_values = []
            for j in window_data:
                rolling_values.append(j[1])


            # compute rolling mean, max, min, and standard deviation
            rolling_mean = statistics.mean(rolling_values)
            rolling_max = max(rolling_values)
            rolling_min = min(rolling_values)
            rolling_stdev = statistics.stdev(rolling_values)

            # gain each windows last date of entry with index -1 and 0th index for date
            current_date = window_data[-1][0]

            # append each values to its ts data frame
            ts_min_data.append((current_date, rolling_min))
            ts_max_data.append((current_date, rolling_max))
            ts_mean_data.append((current_date, rolling_mean))
            ts_stdev_data.append((current_date, rolling_stdev))

        # plotting
        plot_rolling_statistics('GOOG Stock Price', ts, userinput_window_size,
                                ts_min_data, ts_max_data, ts_mean_data, ts_stdev_data)
    except ValueError:
        print('Please enter integer')

main()



