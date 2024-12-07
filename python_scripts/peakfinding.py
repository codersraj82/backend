import sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def find_peaks_in_intensity_range(
    input_file, output_pdf, output_image,
     # min_theta, max_theta, min_intensity,max_intensity, max_peaks, height, distance):
    
    min_theta=20, max_theta=80, min_intensity=200,
    max_intensity=20000, max_peaks=11, height=200, distance=5):
    
    # Load the CSV file
    data = pd.read_csv(input_file)
    
    # Ensure the necessary columns exist
    if '2theta' not in data.columns or 'intensity' not in data.columns:
        raise ValueError("CSV must contain 'theta' and 'intensity' columns")
    
    theta = data['2theta']
    intensity = data['intensity']
    
    # Filter data based on theta and intensity ranges
    filtered_data = data[(theta >= min_theta) & (theta <= max_theta)]
    filtered_data = filtered_data[(filtered_data['intensity'] >= min_intensity) & 
                                  (filtered_data['intensity'] <= max_intensity)]
    
    # Find peaks in the intensity data
    peaks, _ = find_peaks(filtered_data['intensity'], height=height, distance=distance, 
                           prominence=1, width=1, rel_height=0.5)
    
    # Limit number of peaks to max_peaks
    if len(peaks) > max_peaks:
        peaks = peaks[:max_peaks]
    
    # Plot the data and mark the peaks
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_data['theta'], filtered_data['intensity'], label='Intensity')
    plt.plot(filtered_data['theta'].iloc[peaks], filtered_data['intensity'].iloc[peaks], 
             'ro', label='Peaks')
    plt.xlabel('Theta')
    plt.ylabel('Intensity')
    plt.title('XRD Peak Detection')
    plt.legend()
    
    # Save the plot as both PDF and PNG
    plt.savefig(output_image)
    plt.savefig(output_pdf)

    plt.close()
    print("Plot saved to:", output_pdf, output_image)

if __name__ == "__main__":
    # Get command-line arguments
    input_file = sys.argv[1]
    output_pdf = sys.argv[2]
    output_image = sys.argv[3]
    # min_theta=sys.argv[4]
    # max_theta= sys.argv[5]
    # min_intensity=sys.argv[6]
    # max_intensity=sys.argv[7]
    # max_peaks=sys.argv[8]
    # height=sys.argv[9] 
    # distance=sys.argv[10]
    
    # Call the function with default parameters (can be customized later)
    find_peaks_in_intensity_range(input_file, output_pdf, output_image)
                                  # min_theta,max_theta, min_intensity, max_intensity, max_peaks,height, distance)
