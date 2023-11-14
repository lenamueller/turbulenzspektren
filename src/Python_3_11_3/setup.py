"""
File: setup.py
Author: Lena Müller
Date: November 14, 2023

Description:
This script contains the metadata and the datasets for all experiments.
"""

from Datasets import ExpeDataset, SonicDataset


kernel_size = 10

def create_datasets() -> tuple[list[ExpeDataset], list[SonicDataset]]:
    """Return datasets for all experiments (withoud temporal preselection)."""
    
    expe_datasets = [
        ExpeDataset(fn="../../data/2023_07_08/20230708-1329-Log.txt", start_time="2023-07-08 00:00:00", end_time="2023-07-08 23:59:00"),
        ExpeDataset(fn="../../data/2023_07_11/20230711-0504-Log.txt", start_time="2023-07-11 00:00:00", end_time="2023-07-11 23:59:00"),
        ExpeDataset(fn="../../data/2023_08_11/20230811-0810-Log.txt", start_time="2023-08-11 00:00:00", end_time="2023-08-11 23:59:00"),
        ExpeDataset(fn="../../data/2023_08_12/20230812-0641-Log.txt", start_time="2023-08-12 00:00:00", end_time="2023-08-12 23:59:00"),
        ExpeDataset(fn="../../data/2023_08_14/20230814-0656-Log.txt", start_time="2023-08-14 00:00:00", end_time="2023-08-14 23:59:00"),
    ]
    sonic_datasets = [
        SonicDataset(fn="../../data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat", start_time="2023-07-08 00:00:00", end_time="2023-07-08 23:59:00"),
        SonicDataset(fn="../../data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat", start_time="2023-07-11 00:00:00", end_time="2023-07-11 23:59:00"),
        SonicDataset(fn="../../data/2023_08_11/TOA5_7134.Raw_2023_08_11_0924.dat", start_time="2023-08-11 00:00:00", end_time="2023-08-11 23:59:00"),
        SonicDataset(fn="../../data/2023_08_12/TOA5_7134.Raw_2023_08_12_0755.dat", start_time="2023-08-12 00:00:00", end_time="2023-08-12 23:59:00"),
        SonicDataset(fn="../../data/2023_08_14/TOA5_7134.Raw_2023_08_14_0749.dat", start_time="2023-08-14 00:00:00", end_time="2023-08-14 23:59:00"),
    ]
    return expe_datasets, sonic_datasets

def metadata(puo: str) -> tuple:
    """Return metadata for a given PUO (period under observation)."""

    match puo:
        
        case "PUO_00_0": # no expe data
            expe_fn = "../../data/2023_07_08/20230708-1329-Log.txt"
            sonic_fn = "../../data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat"
            start_date = "2023-07-08 08:25:00"
            end_date =   "2023-07-08 10:10:00"
            date = "08.07.2023"
            day=1
        case "PUO_00_1": # no expe data
            expe_fn = "../../data/2023_07_08/20230708-1329-Log.txt"
            sonic_fn = "../../data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat"
            start_date = "2023-07-08 11:30:00"
            end_date =   "2023-07-08 12:45:00"
            date = "08.07.2023"
            day=1
        case "PUO_01":
            expe_fn = "../../data/2023_07_08/20230708-1329-Log.txt"
            sonic_fn = "../../data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat"
            start_date = "2023-07-08 13:30:00"
            end_date =   "2023-07-08 16:10:00"
            date = "08.07.2023"
            day=1
        case "PUO_02":
            expe_fn = "../../data/2023_07_11/20230711-0504-Log.txt"
            sonic_fn = "../../data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat"
            start_date = "2023-07-11 05:05:00"
            end_date =   "2023-07-11 07:00:00"
            date = "11.07.2023"
            day=2
        case "PUO_03": # GAS
            expe_fn = "../../data/2023_07_11/20230711-0504-Log.txt"
            sonic_fn = "../../data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat"
            start_date = "2023-07-11 10:00:00"
            end_date =   "2023-07-11 11:00:00"
            date = "11.07.2023"
            day=2
        case "PUO_04":
            expe_fn = "../../data/2023_07_11/20230711-0504-Log.txt"
            sonic_fn = "../../data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat"
            start_date = "2023-07-11 11:36:00"
            end_date =   "2023-07-11 12:36:00"
            date = "11.07.2023"
            day=2
        case "PUO_05":
            expe_fn = "../../data/2023_08_11/20230811-0810-Log.txt"
            sonic_fn = "../../data/2023_08_11/TOA5_7134.Raw_2023_08_11_0924.dat"
            start_date = "2023-08-11 08:25:00"
            end_date =   "2023-08-11 09:55:00"
            date = "11.08.2023"
            day=3
        case "PUO_06":
            expe_fn = "../../data/2023_08_11/20230811-0810-Log.txt"
            sonic_fn = "../../data/2023_08_11/TOA5_7134.Raw_2023_08_11_0924.dat"
            start_date = "2023-08-11 12:20:00"
            end_date =   "2023-08-11 16:50:00"
            date = "11.08.2023"
            day=3
        case "PUO_07":
            expe_fn = "../../data/2023_08_12/20230812-0641-Log.txt"
            sonic_fn = "../../data/2023_08_12/TOA5_7134.Raw_2023_08_12_0755.dat"
            start_date = "2023-08-12 06:55:00"
            end_date = "2023-08-12 14:20:00"
            date = "12.08.2023"
            day=4
        case "PUO_08":
            expe_fn = "../../data/2023_08_14/20230814-0656-Log.txt"
            sonic_fn = "../../data/2023_08_14/TOA5_7134.Raw_2023_08_14_0749.dat"
            start_date = "2023-08-14 07:00:00"
            end_date =   "2023-08-14 16:55:00"
            date = "14.08.2023"
            day=5
        
    return expe_fn, sonic_fn, start_date, end_date, date, day