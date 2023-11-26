variables = {"EXPE": ["t"], "SONIC": ["t", "wind_z", "wind_h"]}

labels = {
    "t": "Temperatur [°C]",
    "wind_z": "Vertikalwind [m/s]",
    "wind_h": "Horizontalwind [m/s]"
    }

TAPERING_SIZE = 0.1
KERNEL_SIZE = 10
WINDOWS_MIN = [1, 2, 3, 5, 10, 20, 30]
SAMPLE_RATE = {"EXPE": 1, "SONIC": 2}


unique_dates = ["08.07.2023", "11.07.2023", "11.08.2023", "12.08.2023", "14.08.2023"]

all_puos = ["PUO_01", "PUO_02", "PUO_03", "PUO_04", "PUO_05", "PUO_06", 
            "PUO_07", "PUO_08", "PUO_09", "PUO_10", "PUO_11"]


def metadata(period: str) -> tuple:
    """
    Return metadata for a given period. The period can be a whole day or a
    period under observation (PUO).
    """

    match period:
        
        # -------------------------------------------------------------------------
        # whole days
        # -------------------------------------------------------------------------
        
        case "Day1":
            expe_fn =           "data/raw_data/2023_07_08/20230708-1329-Log.txt"
            sonic_fn =          "data/raw_data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat"
            start_datetime =    "2023-07-08 00:00:00"
            end_datetime =      "2023-07-08 23:59:00"
            date =              "08.07.2023"
            day =               1
        case "Day2":
            expe_fn =           "data/raw_data/2023_07_11/20230711-0504-Log.txt"
            sonic_fn =          "data/raw_data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat"
            start_datetime =    "2023-07-11 00:00:00"
            end_datetime =      "2023-07-11 23:59:00"
            date =              "11.07.2023"
            day =               2
        case "Day3":
            expe_fn =           "data/raw_data/2023_08_11/20230811-0810-Log.txt"
            sonic_fn =          "data/raw_data/2023_08_11/TOA5_7134.Raw_2023_08_11_0924.dat"
            start_datetime =    "2023-08-11 00:00:00"
            end_datetime =      "2023-08-11 23:59:00"
            date =              "11.08.2023"
            day =               3
        case "Day4":
            expe_fn =           "data/raw_data/2023_08_12/20230812-0641-Log.txt"
            sonic_fn =          "data/raw_data/2023_08_12/TOA5_7134.Raw_2023_08_12_0755.dat"
            start_datetime =    "2023-08-12 00:00:00"
            end_datetime =      "2023-08-12 23:59:00"
            date =              "12.08.2023"
            day =               4
        case "Day5":
            expe_fn =           "data/raw_data/2023_08_14/20230814-0656-Log.txt"
            sonic_fn =          "data/raw_data/2023_08_14/TOA5_7134.Raw_2023_08_14_0749.dat"
            start_datetime =    "2023-08-14 00:00:00"
            end_datetime =      "2023-08-14 23:59:00"
            date =              "14.08.2023"
            day =               5
        
        # -------------------------------------------------------------------------
        # periods under observation
        # -------------------------------------------------------------------------
        
        case "PUO_00_0": # no expe data
            expe_fn =           "data/raw_data/2023_07_08/20230708-1329-Log.txt"
            sonic_fn =          "data/raw_data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat"
            start_datetime =    "2023-07-08 08:25:00" # min: 2023-07-08 08:25:00
            end_datetime =      "2023-07-08 10:10:00" # max: 2023-07-08 10:10:00
            date =              "08.07.2023"
            day =               1
        case "PUO_00_1": # no expe data
            expe_fn =           "data/raw_data/2023_07_08/20230708-1329-Log.txt"
            sonic_fn =          "data/raw_data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat"
            start_datetime =    "2023-07-08 11:30:00" # min: 2023-07-08 11:30:00
            end_datetime =      "2023-07-08 12:45:00" # max: 2023-07-08 12:45:00
            date =              "08.07.2023"
            day =               1
        case "PUO_01":
            expe_fn =           "data/raw_data/2023_07_08/20230708-1329-Log.txt"
            sonic_fn =          "data/raw_data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat"
            start_datetime =    "2023-07-08 13:30:00" # min: 2023-07-08 13:30:00
            end_datetime =      "2023-07-08 15:00:00" # max: 2023-07-08 16:10:00
            date =              "08.07.2023"
            day =               1
        case "PUO_02":
            expe_fn =           "data/raw_data/2023_07_11/20230711-0504-Log.txt"
            sonic_fn =          "data/raw_data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat"
            start_datetime =    "2023-07-11 06:15:00" # min: 2023-07-11 05:05:00
            end_datetime =      "2023-07-11 07:00:00" # max: 2023-07-11 07:00:00
            date =              "11.07.2023"
            day =               2
        case "PUO_03": # GAS
            expe_fn =           "data/raw_data/2023_07_11/20230711-0504-Log.txt"
            sonic_fn =          "data/raw_data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat"
            start_datetime =    "2023-07-11 10:00:00" # min: 2023-07-11 10:00:00
            end_datetime =      "2023-07-11 11:00:00" # max: 2023-07-11 11:00:00
            date =              "11.07.2023"
            day =               2
        case "PUO_04":
            expe_fn =           "data/raw_data/2023_07_11/20230711-0504-Log.txt"
            sonic_fn =          "data/raw_data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat"
            start_datetime =    "2023-07-11 11:36:00" # min: 2023-07-11 11:36:00
            end_datetime =      "2023-07-11 12:36:00" # max: 2023-07-11 12:36:00
            date =              "11.07.2023"
            day =               2
        case "PUO_05":
            expe_fn =           "data/raw_data/2023_08_11/20230811-0810-Log.txt"
            sonic_fn =          "data/raw_data/2023_08_11/TOA5_7134.Raw_2023_08_11_0924.dat"
            start_datetime =    "2023-08-11 08:25:00" # min: 2023-08-11 08:25:00
            end_datetime =      "2023-08-11 09:55:00" # max: 2023-08-11 09:55:00
            date =              "11.08.2023"
            day =               3
        case "PUO_06":
            expe_fn =           "data/raw_data/2023_08_11/20230811-0810-Log.txt"
            sonic_fn =          "data/raw_data/2023_08_11/TOA5_7134.Raw_2023_08_11_0924.dat"
            start_datetime =    "2023-08-11 12:20:00" # min: 2023-08-11 12:20:00
            end_datetime =      "2023-08-11 14:00:00" # max: 2023-08-11 16:50:00
            date =              "11.08.2023"
            day =               3
        case "PUO_07":
            expe_fn =           "data/raw_data/2023_08_11/20230811-0810-Log.txt"
            sonic_fn =          "data/raw_data/2023_08_11/TOA5_7134.Raw_2023_08_11_0924.dat"
            start_datetime =    "2023-08-11 15:45:00" # min: 2023-08-11 12:20:00
            end_datetime =      "2023-08-11 16:45:00" # max: 2023-08-11 16:50:00
            date =              "11.08.2023"
            day =               3
        case "PUO_08":
            expe_fn =           "data/raw_data/2023_08_12/20230812-0641-Log.txt"
            sonic_fn =          "data/raw_data/2023_08_12/TOA5_7134.Raw_2023_08_12_0755.dat"
            start_datetime =    "2023-08-12 08:00:00" # min: 2023-08-12 06:55:00
            end_datetime =      "2023-08-12 09:45:00" # max: 2023-08-12 14:20:00
            date =              "12.08.2023"
            day =               4
        case "PUO_09":
            expe_fn =           "data/raw_data/2023_08_12/20230812-0641-Log.txt"
            sonic_fn =          "data/raw_data/2023_08_12/TOA5_7134.Raw_2023_08_12_0755.dat"
            start_datetime =    "2023-08-12 12:00:00" # min: 2023-08-12 06:55:00
            end_datetime =      "2023-08-12 13:00:00" # max: 2023-08-12 14:20:00
            date =              "12.08.2023"
            day =               4
        case "PUO_10":
            expe_fn =           "data/raw_data/2023_08_14/20230814-0656-Log.txt"
            sonic_fn =          "data/raw_data/2023_08_14/TOA5_7134.Raw_2023_08_14_0749.dat"
            start_datetime =    "2023-08-14 08:00:00" # min: 2023-08-14 07:00:00
            end_datetime =      "2023-08-14 09:30:00" # max: 2023-08-14 16:55:00
            date =              "14.08.2023"
            day =               5
        case "PUO_11":
            expe_fn =           "data/raw_data/2023_08_14/20230814-0656-Log.txt"
            sonic_fn =          "data/raw_data/2023_08_14/TOA5_7134.Raw_2023_08_14_0749.dat"
            start_datetime =    "2023-08-14 12:45:00" # min: 2023-08-14 07:00:00
            end_datetime =      "2023-08-14 14:20:00" # max: 2023-08-14 16:55:00
            date =              "14.08.2023"
            day =               5
        
    return expe_fn, sonic_fn, start_datetime, end_datetime, date, day


import scipy.signal.windows as wf

window_functions = [
    # No parameters:
    wf.boxcar, wf.exponential, wf.blackman, wf.blackmanharris, 
    wf.bohman, wf.barthann, wf.cosine, wf.flattop, wf.hamming, wf.hann, 
    wf.lanczos, wf.nuttall, wf.parzen, wf.taylor, wf.triang, wf.tukey,
    
    # Need parameters:
    # wf.chebwin, wf.dpss, wf.gaussian, wf.general_cosine, wf.general_gaussian,
    # wf.general_hamming, wf.kaiser, wf.kaiser_bessel_derived, 
    ]
