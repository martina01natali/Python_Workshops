"""
Library: lib_datasets_IrrigationItaly.py
Author(s): Martina Natali (martinanatali@cnr.it)
Date: 2024-03-18
Version: 1.0.0
"""

import netCDF4 as nc
import xarray as xr
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
def read_nc(file_sm, data_settings):

    assign_variables(data_settings)
    ds = nc.Dataset(file_sm)

    # explore description
    print(ds.title, '\n')
    print(ds.description, '\n')
    print(ds.creation_time, '\n')
    print(ds.creator_institution, '\n')
    # ds['Time_days_1'] # this gives information on the variable
    # ds['Time_days_1'][:] # this gives the array of values, which is a masked array
    # ds['Time_days_1'][:].data # this accesses the underlying data in the masked array

    # list and count number of sites
    print('Number of sites: ', len(np.unique([key.split('_')[-1] for key in ds.variables])))

    # retrieve list of variables
    ds_vars = [k for k in ds.variables] # ds.variables returns a dict


    # select variables for a single field (field_id)
    pattern = field_id
    ds_vars_1 = [k for k in ds_vars if pattern in k]


    # build dataframe for chosen field (field_id)
    # some variables are in Time_days, others are in time_hours,
    # so the datasets have to be built separately and then merged
    df_days_dict = {
        k:ds[k][:].data for k in cols_in_sm_day
    }
    df_hours_dict = {
        k:ds[k][:].data for k in cols_in_sm_hour
    }

    df_days  = pd.DataFrame.from_dict(df_days_dict)
    df_hours = pd.DataFrame.from_dict(df_hours_dict)
    df_days = df_days.rename(columns={
        cols_in_sm_day[i]:cols_out_sm_day[i] for i in range(len(cols_in_sm_day))
    })
    df_hours = df_hours.rename(columns={
        cols_in_sm_hour[i]:cols_out_sm_hour[i] for i in range(len(cols_in_sm_hour))
    })


    # clean timestamps and set as index
    var_days = cols_out_sm_day[0]
    var_hours = cols_out_sm_hour[0]
    df_days['datetime']  = df_days[var_days].apply(lambda x : pd.to_datetime(x, unit='D', origin=pd.Timestamp('2000-01-01')))
    df_hours['datetime'] = df_hours[var_hours].apply(lambda x : pd.to_datetime(x, unit='D', origin=pd.Timestamp('2000-01-01')).round('H'))
    df_days.set_index('datetime', inplace=True)
    df_hours.set_index('datetime', inplace=True)


    # build hourly dataset
    df_hours = df_hours.merge(df_days.resample('h').asfreq(), left_on=var_hours, right_on=var_days)


    # clean temperatures from K to °C
    var_temp = 'temperature'
    df_hours[var_temp] = df_hours[var_temp].apply(lambda x : x-273.16)
    df_hours['temperature_min'] = df_hours.groupby(df_hours.index.date)['temperature'].transform('min')
    df_hours['temperature_max'] = df_hours.groupby(df_hours.index.date)['temperature'].transform('max')


    # clean from fillvalue -9999 and substitute with nan
    df_hours = df_hours.replace(-9999, np.nan)


    # retrieve average lons and lats
    lat_centroid = np.nanmean(ds['Latitude_'+pattern][:].data)
    lon_centroid = np.nanmean(ds['Longitude_'+pattern][:].data)
    
    return df_hours, lat_centroid, lon_centroid


# ----------------------------------------------------------------------------
# read sigma0 data

def read_nc_s0(file_sigma0, data_settings):

    assign_variables(data_settings)
    df_s0 = None
    for f in file_sigma0:
        f_id = ('_').join(f.split('/')[-1].split('.')[-2].split('_')[1:])
        ds = xr.open_dataset(f)
        df = ds.to_dataframe().reset_index()
        df = df.rename(columns={cols_in_sigma0[i]:cols_out_sigma0[i] for i in range(len(cols_in_sigma0))})
        df = df.set_index('datetime')
        df = df.resample('D').mean().dropna()
        if df_s0 is None:
            df_s0 = df.copy()
            f_id_first = f_id
        else:
            df_s0 = df_s0.merge(df, on='datetime', suffixes=('_'+f_id_first, '_'+f_id))
    return df_s0


# ----------------------------------------------------------------------------
# read ndvi data
def read_nc_ndvi(file_ndvi, data_settings):
    
    assign_variables(data_settings)
    df_ndvi = None
    for f in file_ndvi:
        f_id = ('_').join(f.split('/')[-1].split('.')[-2].split('_')[1:])
        ds = xr.open_dataset(f)
        df = ds.to_dataframe().reset_index()
        df = df.rename(columns={cols_in_sigma0[i]:cols_out_sigma0[i] for i in range(len(cols_in_sigma0))})
        df = df.set_index('datetime')
        df = df.resample('D').mean().dropna()
        df = pd.DataFrame(df['NDVI'])
        if df_ndvi is None:
            df_ndvi = df.copy()
            f_id_first = f_id
        else:
            df_ndvi = df_ndvi.merge(df, on='datetime', suffixes=('_'+f_id_first, '_'+f_id))
    return df_ndvi


# ----------------------------------------------------------------------------
# read output nc file
def read_nc_output(filename_output):
    
    field_id = filename_output.split('_')[4]
    ds = xr.open_dataset(filename_output)
    df = ds.to_dataframe().reset_index()
    df = df.rename(columns={col:col.replace('_'+field_id, '') for col in df.columns})
    df = df.set_index('Datetime')
    return field_id, df


# ----------------------------------------------------------------------------
# aux function to define variables from configuration file
# DO NOT REMOVE: it's needed in this module to make the other functions work

def assign_variables(config_dict, prefix=''):
    var_dict = {}
    """Warning: this function works on the global() namespace of the module in which it is defined"""
    for key, value in config_dict.items():
        if isinstance(value, dict):
            # For nested dictionaries, add the current key to the prefix and recursively call the function
            assign_variables(value, prefix=prefix)
        else:
            # Assign the value to a global variable with the constructed name
            name_var = key
            if value=='True': value=True
            elif value=='False': value=False
            globals().update({name_var:value})
            del name_var