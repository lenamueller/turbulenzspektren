
def metadata(measuring_situation: str) -> tuple:
    """Return metadata for a given measuring situation."""

    match measuring_situation:
        
        # day 1
        case "ES_2023_07_08_morning":
            expe_fn = "../../data/2023_07_08/20230708-1329-Log.txt"
            sonic_fn = "../../data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat"
            start_date = "2023-07-08 08:25:00"
            end_date =   "2023-07-08 10:10:00"
            date = "08.07.2023"
        case "ES_2023_07_08_noon":
            expe_fn = "../../data/2023_07_08/20230708-1329-Log.txt"
            sonic_fn = "../../data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat"
            start_date = "2023-07-08 11:30:00"
            end_date =   "2023-07-08 12:45:00"
            date = "08.07.2023"
        case "ES_2023_07_08_afternoon":
            expe_fn = "../../data/2023_07_08/20230708-1329-Log.txt"
            sonic_fn = "../../data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat"
            start_date = "2023-07-08 13:30:00"
            end_date =   "2023-07-08 16:10:00"
            date = "08.07.2023"
        
        # day 2
        case "ES_2023_07_11_morning":
            expe_fn = "../../data/2023_07_11/20230711-0504-Log.txt"
            sonic_fn = "../../data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat"
            start_date = "2023-07-11 05:05:00"
            end_date =   "2023-07-11 07:00:00"
            date = "09.07.2023"
        case "GAS_2023_07_11_noon":
            expe_fn = "../../data/2023_07_11/20230711-0504-Log.txt"
            sonic_fn = "../../data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat"
            start_date = "2023-07-11 10:00:00"
            end_date =   "2023-07-11 11:00:00"
            date = "11.07.2023"
        case "ES_2023_07_11_noon":
            expe_fn = "../../data/2023_07_11/20230711-0504-Log.txt"
            sonic_fn = "../../data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat"
            start_date = "2023-07-11 11:36:00"
            end_date =   "2023-07-11 12:36:00"
            date = "11.07.2023"
    
        # TODO: #1 update metadata for day 3
        
    return expe_fn, sonic_fn, start_date, end_date, date