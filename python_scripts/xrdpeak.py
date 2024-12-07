import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# Read the CSV file
file_path = r"C:\Users\Sarfaraz Shaikh\Desktop\Hematite_CSV.csv"  # Adjust the file path as needed
xrd_data = pd.read_csv(file_path, header=0)

# Strip spaces from column names
xrd_data.columns = xrd_data.columns.str.strip()

# Check if the required columns are present
if '2theta' not in xrd_data.columns or 'Intensity' not in xrd_data.columns:
    print("Error: Missing required columns ('2theta', 'Intensity') in the CSV file.")
else:
    # Drop rows with missing values
    xrd_data = xrd_data.dropna(subset=['2theta', 'Intensity'])

    # Extract '2theta' and 'Intensity' columns
    theta = xrd_data['2theta']
    intensity = xrd_data['Intensity']

    # Filter the data to include only 2-theta values between 20° and 70°
    filtered_data = xrd_data[(theta >= 20) & (theta <= 70)]
    filtered_theta = filtered_data['2theta']
    filtered_intensity = filtered_data['Intensity']

    # Find peaks in the filtered intensity data
    peaks, properties = find_peaks(filtered_intensity, height=200, prominence=50)  # Adjust thresholds as needed

    # Extract the highest-intensity peak
    if len(peaks) == 0:
        print("No peaks found.")
    else:
        # Get the index of the highest peak
        max_peak_index = np.argmax(properties['peak_heights'])
        peak_position = filtered_theta.iloc[peaks[max_peak_index]]
        peak_intensity = properties['peak_heights'][max_peak_index]

        # Calculate half maximum
        half_max = peak_intensity / 2

        # Interpolate around the peak to find FWHM
        interp_func = interp1d(filtered_theta, filtered_intensity, kind='linear', bounds_error=False, fill_value=0)

        # Generate finer theta values around the peak
        fine_theta = np.linspace(peak_position - 1, peak_position + 1, 1000)
        fine_intensity = interp_func(fine_theta)

        # Find where intensity crosses the half max value
        left_idx = np.where(fine_intensity >= half_max)[0][0]  # First point where intensity is >= half max
        right_idx = np.where(fine_intensity >= half_max)[0][-1]  # Last point where intensity is >= half max

        # Calculate FWHM
        fwhm = fine_theta[right_idx] - fine_theta[left_idx]

        # Print the results
        print(f"Highest Peak Position (2θ): {peak_position:.2f}°")
        print(f"Peak Intensity: {peak_intensity:.2f}")
        print(f"FWHM: {fwhm:.2f}°")

        # Plot the XRD data with annotations
        plt.figure(figsize=(10, 6))
        plt.plot(filtered_theta, filtered_intensity, label='XRD Pattern', color='blue')
        plt.axvline(x=peak_position, color='red', linestyle='--', label=f'Peak at {peak_position:.2f}°')
        plt.hlines(y=half_max, xmin=fine_theta[left_idx], xmax=fine_theta[right_idx], color='green',
                   linestyle='--', label=f'FWHM = {fwhm:.2f}°')
        plt.title("XRD Pattern with FWHM Calculation")
        plt.xlabel("2θ (degrees)")
        plt.ylabel("Intensity (a.u.)")
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()