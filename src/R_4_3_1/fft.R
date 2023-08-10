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