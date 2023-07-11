rm(list=ls())
setwd("Documents/Studium/Master_Hydrologie/VertiefungspraxisMeteo")
getwd()

source("code/read_sensor_expe.R")
source("code/plot_sensor_expe.R")
source("code/fft.R")

fn_data <- "data/2023_07_08/20230708-1329-Log.txt"
fn_plot <- "images/Plot_23_07_08.png"
sensor0 = read_sensor_expe(fn=fn_data, sensorid=0)
plot_sensor_expe(
    sensor_data=sensor0, plot_fn=fn_plot, 
    start_time="00:00", end_time="23:59"
    )

fn_data <- "data/2023_07_11/20230711-0504-Log.txt"
fn_plot <- "images/Plot_23_07_11.png"
sensor0 = read_sensor_expe(fn=fn_data, sensorid=0)
plot_sensor_expe(
    sensor_data=sensor0, plot_fn=fn_plot, 
    start_time="10:10", end_time="11:10"
    )

