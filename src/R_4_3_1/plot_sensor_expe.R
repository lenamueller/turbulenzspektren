df_subset <- function(sensor_data, start_date, end_date) {
    sensor_data <- subset(sensor_data, datetime > start_date)
    sensor_data <- subset(sensor_data, datetime < end_date)
    return(sensor_data)
}

plot_sensor_expe <- function(
        sensor_data,
        plot_fn,
        start_time,
        end_time
        ) {
    # Plotting dirunal curves and FFT of temperature, rel. humidity and 
    # pressure.
    
    # read date
    date <- as.Date(sensor_data$datetime[1], "CEST")
    
    # subset data to one hour
    sensor_data <-df_subset(
        sensor_data,
        start_date = as.POSIXct(paste(date, start_time, sep=" ")),
        end_date = as.POSIXct(paste(date, end_time, sep=" ")) 
    )
    
    # configure plot
    png(file=plot_fn, width = 3000, height = 2000, res = 250, units = "px")
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