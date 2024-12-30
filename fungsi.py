from pandas import DataFrame, Series
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from datetime import datetime

def persiapan(folder_data):
    df_climate_data_staging = pd.read_csv(f'{folder_data}/climate_data.csv')
    df_climate_data_staging.head()

    kolom_pengganti = {
        'Tn': 'suhu_min',
        'Tx': 'suhu_maks',
        'Tavg': 'suhu_rata2',
        'RH_avg': 'kelembaban_rata2',
        'RR': 'curah_hujan',
        'ss': 'durasi_sinar_matahari_jam',
        'ff_x': 'kecepatan_angin_maks',
        'ddd_x': 'arah_angin_kecepatan_maks',
        'ff_avg': 'kecepatan_angin_rata2',
        'ddd_car': 'arah_angin_tersering',
        'station_id': 'id_stasiun',
        'date': 'tanggal_pencatatan'
    }

    df_climate_data = df_climate_data_staging.rename(columns=kolom_pengganti)
    df_provinces = pd.read_csv(f'{folder_data}/province_detail.csv')
    df_stations = pd.read_csv(f'{folder_data}/station_detail.csv')

    '''
    Pengaturan - Transformasi
    '''

    # mengubah format datetime menjadi format US
    df_climate_data = df_climate_data.assign(tanggal_pencatatan=df_climate_data['tanggal_pencatatan'].apply(lambda x: datetime.strptime(x, '%d-%m-%Y')))

    # mengonversi indeks ke tipe DatetimeIndex
    df_climate_data.set_index(pd.DatetimeIndex(df_climate_data.index)) 

    # menghasilkan set denormalisasi dengan menggabungkan semua dataframe
    df_climate_data = df_climate_data\
        .merge(df_stations, how='inner', left_on='id_stasiun', right_on='station_id')\
            .merge(df_provinces, how='inner', left_on='province_id', right_on='province_id')
    

    '''
    Memfilter suhu ekstrem dari grafik:
    '''
    df_climate_data = df_climate_data[(df_climate_data.suhu_min > 0) & (df_climate_data.suhu_maks < 50)]
    df_climate_data = df_climate_data[(df_climate_data.suhu_rata2 > 0) & (df_climate_data.suhu_rata2 < 50)]
    df_climate_data = df_climate_data[(df_climate_data.kelembaban_rata2 <= 100)]
    df_climate_data = df_climate_data[(df_climate_data.suhu_maks > df_climate_data.suhu_min)]

    df_climate_data = df_climate_data[df_climate_data.curah_hujan < 500]    

    return df_climate_data

def plot_time_series(df_cuaca, variabel):
    """
    Plots the time series for a specific variable in the cuaca DataFrame.

    Args:
        df_cuaca (pandas.DataFrame): The cuaca DataFrame containing weather data.
        variabel (str): The name of the variable to plot (e.g., "suhu", "kelembapan").

    Returns:
        None
    """

    # Validate variable name
    valid_variables = ["suhu", "kelembaban", "curah_hujan", "durasi_sinar_matahari_jam", "kecepatan_angin"]
    if variabel not in valid_variables:
        raise ValueError(f"Invalid variable name: {variabel}. Valid options are: {', '.join(valid_variables)}")

    # Perform aggregation using separate function (optional)
    # df_agg = aggregate_data(df_cuaca, variabel)  # If you have a separate function

    # Aggregate data using NamedAgg
    if variabel == "suhu":
        agg_dict = {
            f"{variabel}_min": pd.NamedAgg(column=f"{variabel}_min", aggfunc="min"),
            f"{variabel}_maks": pd.NamedAgg(column=f"{variabel}_maks", aggfunc="max"),
            f"{variabel}_rata2": pd.NamedAgg(column=f"{variabel}_rata2", aggfunc="mean"),
            f"{variabel}_count": pd.NamedAgg(column=f"{variabel}_rata2", aggfunc="count"),
        }
    elif variabel == "kelembaban" or variabel == "kecepatan_angin":
         agg_dict = {
            f"{variabel}_min": pd.NamedAgg(column=f"{variabel}_rata2", aggfunc="min"),
            f"{variabel}_maks": pd.NamedAgg(column=f"{variabel}_rata2", aggfunc="max"),
            f"{variabel}_rata2": pd.NamedAgg(column=f"{variabel}_rata2", aggfunc="mean"),
            f"{variabel}_count": pd.NamedAgg(column=f"{variabel}_rata2", aggfunc="count"),
        }       
    else:
         agg_dict = {
            f"{variabel}_min": pd.NamedAgg(column=variabel, aggfunc="min"),
            f"{variabel}_maks": pd.NamedAgg(column=variabel, aggfunc="max"),
            f"{variabel}_rata2": pd.NamedAgg(column=variabel, aggfunc="mean"),
            f"{variabel}_count": pd.NamedAgg(column=variabel, aggfunc="count"),
        }       
    df_cuaca = df_cuaca.set_index('tanggal_pencatatan')
    df_agg = df_cuaca.groupby('tanggal_pencatatan').agg(**agg_dict)
    df_agg = df_agg.resample('ME').agg({
            f"{variabel}_min": 'mean',  # Average of daily minimums
            f"{variabel}_maks": 'mean',  # Average of daily maximums
            f"{variabel}_rata2": 'mean',  # Average of daily means
            f"{variabel}_count": 'sum'   # Sum of daily counts
        })
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))  # Create figure and axes object
    ax.plot(df_agg[f"{variabel}_rata2"], label='Rata-rata')
    ax.fill_between(
        df_agg.index,
        df_agg[f"{variabel}_min"],
        df_agg[f"{variabel}_maks"],
        alpha=0.2,
        label='Rentang'
    )
    ax.set_xlabel('Tanggal')
    ax.set_ylabel(f"{variabel}") 
    ax.set_title(f'Perubahan {variabel}')
    ax.legend()
    ax.grid(True)

    return fig  # Return the figure object

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_time_series_plotly(df_cuaca, variabel):
    """
    Plots the time series for a specific variable in the cuaca DataFrame using Plotly.

    Args:
        df_cuaca (pandas.DataFrame): The cuaca DataFrame containing weather data.
        variabel (str): The name of the variable to plot.

    Returns:
        plotly.graph_objects.Figure: The Plotly figure object.
        or None if invalid variabel
    """

    valid_variables = ["suhu", "kelembaban", "curah_hujan", "durasi_sinar_matahari_jam", "kecepatan_angin"]
    if variabel not in valid_variables:
        print(f"Invalid variable name: {variabel}. Valid options are: {', '.join(valid_variables)}")
        return None

    if variabel == "suhu":
        agg_dict = {
            f"{variabel}_min": pd.NamedAgg(column=f"{variabel}_min", aggfunc="min"),
            f"{variabel}_maks": pd.NamedAgg(column=f"{variabel}_maks", aggfunc="max"),
            f"{variabel}_rata2": pd.NamedAgg(column=f"{variabel}_rata2", aggfunc="mean"),
            f"{variabel}_count": pd.NamedAgg(column=f"{variabel}_rata2", aggfunc="count"),
        }
    elif variabel == "kelembaban" or variabel == "kecepatan_angin":
         agg_dict = {
            f"{variabel}_min": pd.NamedAgg(column=f"{variabel}_rata2", aggfunc="min"),
            f"{variabel}_maks": pd.NamedAgg(column=f"{variabel}_rata2", aggfunc="max"),
            f"{variabel}_rata2": pd.NamedAgg(column=f"{variabel}_rata2", aggfunc="mean"),
            f"{variabel}_count": pd.NamedAgg(column=f"{variabel}_rata2", aggfunc="count"),
        }       
    else:
         agg_dict = {
            f"{variabel}_min": pd.NamedAgg(column=variabel, aggfunc="min"),
            f"{variabel}_maks": pd.NamedAgg(column=variabel, aggfunc="max"),
            f"{variabel}_rata2": pd.NamedAgg(column=variabel, aggfunc="mean"),
            f"{variabel}_count": pd.NamedAgg(column=variabel, aggfunc="count"),
        }       
    df_cuaca = df_cuaca.set_index('tanggal_pencatatan')
    df_agg = df_cuaca.groupby('tanggal_pencatatan').agg(**agg_dict)
    df_agg = df_agg.resample('ME').agg({
            f"{variabel}_min": 'mean',
            f"{variabel}_maks": 'mean',
            f"{variabel}_rata2": 'mean',
            f"{variabel}_count": 'sum'
        })

    fig = make_subplots(specs=[[{"secondary_y": False}]])

    fig.add_trace(go.Scatter(x=df_agg.index, y=df_agg[f"{variabel}_rata2"], name='Rata-rata', line=dict(color='blue')), secondary_y=False)
    fig.add_trace(go.Scatter(x=df_agg.index, y=df_agg[f"{variabel}_maks"], name='Maks', line=dict(color='lightgray', width=0), showlegend=False), secondary_y=False)
    fig.add_trace(go.Scatter(x=df_agg.index, y=df_agg[f"{variabel}_min"], name='Min', line=dict(color='lightgray', width=0), fill='tonexty', fillcolor='rgba(0,100,255,0.2)', showlegend=False), secondary_y=False)

    fig.update_layout(
        title=f'Perubahan {variabel}',
        xaxis_title="Periode",
        yaxis_title=f"{variabel}",
        template="plotly_white"  # Use a clean template
    )
    fig.update_xaxes(
        dtick="M6",  # Set monthly ticks
        tickformat="%b %Y",  # Format ticks as "Month Year"
        tickangle=-45
    )
    return fig