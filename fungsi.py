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
        'Tx': 'suhu_max',
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
    df_climate_data = df_climate_data[(df_climate_data.suhu_min > 0) & (df_climate_data.suhu_max < 50)]
    df_climate_data = df_climate_data[(df_climate_data.suhu_rata2 > 0) & (df_climate_data.suhu_rata2 < 50)]
    df_climate_data = df_climate_data[(df_climate_data.kelembaban_rata2 <= 100)]
    df_climate_data = df_climate_data[(df_climate_data.suhu_max > df_climate_data.suhu_min)]

    df_climate_data = df_climate_data[df_climate_data.curah_hujan < 500]    

    return df_climate_data
