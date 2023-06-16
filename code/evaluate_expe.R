rm(list=ls())
setwd("Documents/Studium/Master/VertiefungspraxisMeteo")


fns = c(
    "data/expe/2023/20230412-0714-Log.txt", 
    "data/expe/2023/20230422-0912-Log.txt",
    "data/expe/2023/20230508-1153-Log.txt",
    "data/expe/2023/20230531-0929-Log.txt",
    "data/expe/2023/20230604-0810-Log.txt"
    )

read_sensor_expe <- function(fn, sensorid) {
    # Reading single Sensor data from EXPE
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

Nyquist_frequency <- function(sensor_data) {
    return(length(sensor_data)/2)
}

norm <- function(complex_number) {
    return(Re(complex_number)**2 + Im(complex_number)**2)
}

mult_2 <- function(value){
    return(value*2)
}

calc_fft <- function(sensor_data) {
    
    # Calculate the Nyquist frequency
    n_f <- Nyquist_frequency(sensor_data)
    
    # Calculate the FFT -> complex numbers
    fft_values <- fft(sensor_data, inverse=FALSE)
    
    # Calculate the square of the norm of each complex number
    fft_normed <- lapply(fft_values, norm)
    
    # Remove first element (mean) and numbers beyond Nyquist frequency
    fft_normed_sub <- fft_normed[c(2:n_f)]
    
    # Multiply by 2
    fft_2 = lapply(fft_normed_sub, mult_2)
    
    return(fft_2)
}

df_subset <- function(sensor_data, start_date, end_date) {
    sensor_data <- subset(sensor_data, datetime > start_date)
    sensor_data <- subset(sensor_data, datetime < end_date)
    return(sensor_data)
}

plot_sensor_expe <- function(sensor_data, plot_fn) {
    # Plotting dirunal curves and histogram of temperature, rel. humidity and 
    # pressure.
    
    # read date
    date <- as.Date(sensor_data$datetime[1], "CEST")
    
    # subset data to one hour
    sensor_data <-df_subset(
                    sensor_data,
                    start_date = as.POSIXct(paste(date, "11:00", sep=" ")),
                    end_date = as.POSIXct(paste(date, "12:00", sep=" ")) 
                    )
    
    # start plotting
    png(file=plot_fn, width=1000, height=600, res = 100)
    par(mfrow=c(2,3))
    
    # time series
    plot(sensor_data$datetime, sensor_data$t, type = "line", frame = FALSE, pch = 1, col = "blue", 
         xlab = "time [UTC]", ylab = "temperature [°C]")
    plot(sensor_data$datetime, sensor_data$rh, type = "line", frame = FALSE, pch = 1, col = "blue", 
         xlab = "time [UTC]", ylab = "rel. humidity [%]")
    plot(sensor_data$datetime, sensor_data$p, type = "line", frame = FALSE, pch = 1, col = "blue", 
         xlab = "time [UTC]", ylab = "pressure [hPa]")

    # frequencies
    fft_data <- calc_fft(sensor_data$t)
    plot(c(2:length(fft_data)), fft_data[2:length(fft_data)], t = "h", log="xy", 
         xlab = "n", ylab = "strength")
    fft_data <- calc_fft(sensor_data$rh)
    plot(c(2:length(fft_data)), fft_data[2:length(fft_data)], t = "h", log="xy", 
         xlab = "n", ylab = "strength")
    fft_data <- calc_fft(sensor_data$p)
    plot(c(2:length(fft_data)), fft_data[2:length(fft_data)], t = "h", log="xy", 
         xlab = "n", ylab = "strength")
    
    # Clear the current plot
    dev.off()
}


fns_plot = c("images/Plot_23_04_12.png", "images/Plot_23_04_22.png", 
             "images/Plot_23_05_08.png", "images/Plot_23_05_31.png", 
             "images/Plot_23_06_04.png")

for (i in 1:length(fns)) {
    print(i)
    sensor0 <- read_sensor_expe(fns[i], sensorid=0)
    plot_sensor_expe(sensor_data=sensor0, plot_fn=fns_plot[i])
}

