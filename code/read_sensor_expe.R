read_sensor_expe <- function(fn, sensorid) {
    # Reading single Sensor data from EXPE
    # 
    # Date; Time; Module Address; Module Address; Value1; Value2; Value3; Value4
    # Adress 0: Datum; Zeit; Modul; SensorID; XX; Temperatur in °C*100; 
    #   relativeFeuchte in %*1000; Lufdruck in Pa
    # Adress 2: [Datum; Zeit; Modul; SensorID; XX; Temperatur in °C*100; 
    #   relativeFeuchte in %*1000;  XX
    # Adress 1: [Datum; Zeit; Modul; SensorID; XX; Altitute; Latitude; Longitude
    
    col_names <- c("Date", "Time", "ModAddr", "ModCmd",
                   "Val1", "Val2", "Val3", "Val4")
    dat <- read.table(fn, header = TRUE, sep = ";", skip=2, 
                      col.names = col_names, fill = TRUE)
    
    # data types
    dat$datetime <- paste(dat$Date, dat$Time, sep=" ")
    dat$datetime <- as.POSIXct(dat$datetime,format="%Y-%m-%d %H:%M:%S")
    
    dat$Val1 <- as.numeric(dat$Val1)
    dat$Val2 <- as.numeric(dat$Val2)
    dat$Val3 <- as.numeric(dat$Val3)
    dat$Val4 <- as.numeric(dat$Val4)
    
    # NA
    dat <- na.omit(dat)
    
    # delete unused columns
    dat = subset(dat, select = -c(Date, Time, ModAddr))
    
    # split according to ModCmd
    split_list <- split(dat,dat$ModCmd)
    sensor0 <- as.data.frame(split_list[[1]])
    sensor1 <- as.data.frame(split_list[[2]])
    sensor2 <- as.data.frame(split_list[[3]])
    
    if (sensorid == 0) {
        print(colnames(sensor0))
        colnames(sensor0)[3] ="t"
        colnames(sensor0)[4] ="rh"
        colnames(sensor0)[5] ="p"
        
        print(colnames(sensor0))
        sensor0$t <- sensor0$t / 100
        sensor0$rh <- sensor0$rh / 1000
        sensor0$p <- sensor0$p / 1000
        return(sensor0)
        
    } else if (sensorid == 1) {
        return(sensor1)
        
    }else {
        return(sensor2)
    }
} 