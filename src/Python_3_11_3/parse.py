import pandas as pd
import numpy as np

from setup import metadata


def parse_data(
        device: str, 
        period: str
        ) -> pd.DataFrame | None:
    expe_fn, sonic_fn, start_datetime, end_datetime, _, _ = metadata(period)
    
    if device == "EXPE":
        return _parse_expe(expe_fn, start_datetime, end_datetime)
    elif device == "SONIC":
        return _parse_sonic(sonic_fn, start_datetime, end_datetime)
    else:
        raise ValueError(f"Invalid device '{device}'.")

def get_var(
        device: str,
        period: str,
        var: str
        ) -> np.ndarray:
    """Return a variable for certain period and measuring device as array."""
    df = parse_data(device, period)
    arr = df[var].to_numpy()
    return arr

def _parse_expe(expe_fn: str, start_datetime: str, end_datetime: str) -> pd.DataFrame:
    """Parse the data from the csv-file using sensor 0."""
    
    df = pd.read_csv(expe_fn, delimiter=";")

    sensor0 = df.loc[df['Module Command'] == 0]
    rename_cols = {"Value2":"t", "Value3":"rh", "Value4":"p"}
    type_cols = {'t': float, 'rh': float, 'p': float}
    sensor0 = sensor0.rename(columns=rename_cols).astype(type_cols)

    sensor0["t"] = sensor0["t"]/100
    sensor0["rh"] = sensor0["rh"]/1000
    sensor0["p"] = sensor0["p"]/1000

    sensor0["Datetime"] = sensor0['Date'].astype(str) +" "+ sensor0["Time"]
    sensor0["Datetime"] = pd.to_datetime(sensor0["Datetime"], format="%Y-%m-%d %H:%M:%S")
    sensor0_flt = sensor0.loc[sensor0['Datetime'].between(start_datetime, end_datetime, inclusive="both")]
    sensor0_flt = sensor0_flt[["Datetime", "t", "rh", "p"]]
    
    return sensor0_flt

def _calc_3d_wind(row)-> float:
    """Calculate the absolute wind speed from the 3 wind components."""
    return np.sqrt(row["windx"]**2 + row["windy"]**2 + row["windz"]**2)

def _calc_2d_wind(row)-> float:
    """Calculate the horizontal wind speed from the 3 wind components."""
    return np.sqrt(row["windx"]**2 + row["windy"]**2)

def _parse_sonic(sonic_fn: str, start_datetime: str, end_datetime: str) ->  pd.DataFrame:
    """Parse the data from the dat-file and calculate 2D and 3D wind speed."""
    
    df = pd.read_csv(sonic_fn, delimiter=",", usecols=[0,2,3,4,5], names=["Datetime", "windx", "windy", "windz", "t"], skiprows=4)    
    type_cols = {'windx': float, 'windy': float, 'windz': float, 't': float}
    df = df.astype(type_cols)
    df = df.dropna()

    # Convert local time (wihout summer time) to UTC
    df["Datetime"] = pd.to_datetime(df["Datetime"], format="%Y-%m-%d %H:%M:%S")
    df["Datetime"] = df["Datetime"] - pd.Timedelta(hours=1)

    df_flt = df.loc[df['Datetime'].between(start_datetime, end_datetime, inclusive="both")]

    # Calculate 2D and 3D wind speed speed
    df_flt.loc[:, "wind3d"] = df_flt.apply(_calc_3d_wind, axis=1)
    df_flt.loc[:, "wind2d"] = df_flt.apply(_calc_2d_wind, axis=1)

    df_flt = df_flt[["Datetime", "t", "wind3d", "wind2d"]]

    return df_flt