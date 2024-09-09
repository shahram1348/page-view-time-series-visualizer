import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
plt.ioff()
df = pd.read_csv("fcc-forum-pageviews.csv", index_col='date')
df = df[(df["value"] >= df["value"].quantile(0.025)) & (df["value"] <= df["value"].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(10, 6))
                          
    ax.plot(df.index, df['value'])
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.xticks([0, 400, 800, 1200])

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Prepare data for box plots (this part is done!)   
    df_bar = df.copy()
    
    # Convert the index to DatetimeIndex
    df_bar.index = pd.to_datetime(df_bar.index)
    
    # Now  resample
    monthly_avg = df_bar.resample('ME')['value'].mean()
    
    # Create a new DataFrame from the monthly averages
    df_bar = monthly_avg.reset_index()
    df_bar.columns = ['date', 'monthly_average']
    df_bar['year'] = pd.DatetimeIndex(df_bar.date).year
    # Extract month from the date column and create a custom month order
    df_bar['month'] = pd.to_datetime(df_bar['date']).dt.strftime('%b')
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Group by year and month, then calculate the mean of 'value'
    grouped_df = df_bar.groupby(['year', 'month'])['monthly_average'].mean().unstack()
    
    # Reorder columns based on month_order, only including months present in the data
    present_months = [month for month in month_order if month in grouped_df.columns]
    grouped_df = grouped_df[present_months]
    
    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create a grouped bar plot
    grouped_df.plot(kind='bar', ax=ax, width=0.8)
       
    # Customize the plot
    plt.title('Average Daily Page Views by Year and Month')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=0)
    
    # Add legend with a title, sorted months, and only present months
    handles, labels = ax.get_legend_handles_labels()
    sorted_pairs = sorted(zip(labels, handles), key=lambda pair: month_order.index(pair[0]))
    sorted_labels, sorted_handles = zip(*sorted_pairs)
    plt.legend(sorted_handles, sorted_labels, title='Months', bbox_to_anchor=(0.03, 0.7), loc='center left')
    
    # Adjust layout to prevent cutting off labels
    plt.tight_layout()
       
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig
    

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['date'] = pd.to_datetime(df_box['date'])
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Set up the figure and axes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        
    colors_year = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    # Define colors for each season with different shades for each month
    colors_month = [
        '#8dd3c7', '#a1d8cf', '#b5ddd7',  # Spring (Mar, Apr, May)
        '#fb8072', '#fc9889', '#fdb0a0',  # Summer (Jun, Jul, Aug)
        '#ffffb3', '#ffffc1', '#ffffcf',  # Autumn (Sep, Oct, Nov)
        '#80b1d3', '#93beda', '#a6cbe1'   # Winter (Dec, Jan, Feb)
    ]
    # Year-wise Box Plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1, hue='year', palette=colors_year, legend=False)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # Month-wise Box Plot (Seasonality)
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2,  hue='month', order=month_order, palette=colors_month, legend=False)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

