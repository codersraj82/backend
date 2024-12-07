import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np

def FindPeaksInIntensityRange(df, theta_column, intensity_column, min_theta=20, max_theta=80, min_intensity=200, max_intensity=20000, max_peaks=9, **kwargs):
    """Finds the peaks in XRD data within a specific intensity range and limits to the top peaks."""
    # Filter the DataFrame for the specified 2θ range
    filtered_df = df[(df[theta_column] >= min_theta) & (df[theta_column] <= max_theta)]
    
    # Check if the intensity column exists in the filtered DataFrame
    if intensity_column not in filtered_df.columns:
        raise ValueError(f"Column '{intensity_column}' not found in the data. Please check the column names.")
    
    # Find peaks in the intensity column
    peaks, _ = find_peaks(filtered_df[intensity_column], **kwargs)
    
    # Extract rows corresponding to peaks
    peaks_df = filtered_df.iloc[peaks]
    
    # Filter peaks within the intensity range
    peaks_df = peaks_df[(peaks_df[intensity_column] > min_intensity) & (peaks_df[intensity_column] <= max_intensity)]
    
    # Sort by intensity in descending order and limit to max_peaks
    peaks_df = peaks_df.sort_values(by=intensity_column, ascending=False).head(max_peaks)
    
    # Index the peaks by adding a new column for peak indices
    peaks_df['Peak_Index'] = range(1, len(peaks_df) + 1)
    
    return peaks_df, filtered_df

def calculate_d_spacing(theta_degrees, wavelength=1.5406):
    """Calculates d-spacing using Bragg's Law."""
    # Convert 2θ to θ (in radians)
    theta_radians = np.radians(theta_degrees / 2)
    # Calculate d-spacing using Bragg's Law
    d_spacing = wavelength / (2 * np.sin(theta_radians))
    return d_spacing

# File paths
input_file = r"E:\Knime\Knime software\XRD\SnO2CSV.csv"
output_file = r"E:\Knime\Knime software\XRD\XRD_SnO2_indexed_peaks.csv"

# Read the XRD data
data = pd.read_csv(input_file)

# Clean column names (strip leading/trailing spaces if any)
data.columns = data.columns.str.strip()

# Define the correct 2θ and intensity column names based on your data
theta_column = '2theta'  # Replace with the actual name of the 2θ column
intensity_column = 'Intensity'  # Correct column name for intensity

# Calculate step size of the 2θ column
theta_step = data[theta_column].iloc[1] - data[theta_column].iloc[0]

# Convert 2θ distance (1 degree) to data points
distance_points = int(1.2 / theta_step)

# Find peaks with intensity > 200 and <= 20000 within the 2θ range of 20 to 80
peaks_df, filtered_df = FindPeaksInIntensityRange(
    data,
    theta_column,
    intensity_column,
    min_theta=20,
    max_theta=80,
    min_intensity=200,
    max_intensity=20000,
    max_peaks=11,
    height=200,  # Ensures only peaks above 200 are considered
    distance=distance_points  # Minimum distance between peaks in data points
)

# Calculate d-spacing for each peak
peaks_df['d-spacing (Å)'] = peaks_df[theta_column].apply(calculate_d_spacing)

# Save the peaks data to a new CSV file
peaks_df.to_csv(output_file, index=False)

print(f"Indexed peaks saved to {output_file}")

# Plot the XRD data and the peaks
plt.figure(figsize=(12, 6))
plt.plot(filtered_df[theta_column], filtered_df[intensity_column], label='XRD Data', color='blue')

# Plot the peaks
plt.scatter(peaks_df[theta_column], peaks_df[intensity_column], color='red', label='Filtered Peaks', zorder=5)

# Mark the peaks with their indices
for i, row in peaks_df.iterrows():
    plt.text(row[theta_column], row[intensity_column] + 100, f'{row["Peak_Index"]}', color='black', ha='center')

# Add labels and title
plt.xlabel('2θ (degrees)')
plt.ylabel('Intensity (a.u.)')
plt.title('XRD Graph with Filtered Peaks')

# Display the plot
plt.tight_layout()
plt.legend()
plt.show()
