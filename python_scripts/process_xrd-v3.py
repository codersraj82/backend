import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.interpolate import interp1d
from numpy import trapezoid  # Update import from trapz to trapezoid

def process_xrd(file_path, output_image, output_pdf):
    # Set output encoding to UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Load the XRD data
    data = pd.read_csv(file_path, header=0)
    
    # Strip spaces and standardize column names
    data.columns = data.columns.str.strip().str.lower()

    # Check if required columns are present
    if '2theta' not in data.columns or 'intensity' not in data.columns:
        print("Error: Missing required columns ('2theta', 'Intensity') in the CSV file.")
        print("Available columns:", data.columns.tolist())
        return

    # Extract 2-theta and intensity
    two_theta = data['2theta']
    intensity = data['intensity']

    # Baseline correction (amorphous background estimation)
    baseline = np.min(intensity)

    # Subtract baseline from the intensity
    corrected_intensity = intensity - baseline

    # Integrate total area (crystalline + amorphous)
    total_area = trapezoid(intensity, two_theta)

    # Integrate crystalline area (above the baseline)
    crystalline_area = trapezoid(corrected_intensity, two_theta)

    # Calculate % Crystallinity
    percent_crystallinity = (crystalline_area / total_area) * 100

    # Filter the data to include only 2-theta values between 20° and 70°
    filtered_data = data[(two_theta >= 20) & (two_theta <= 70)]
    filtered_theta = filtered_data['2theta']
    filtered_intensity = filtered_data['intensity']

    # Find peaks in the filtered intensity data
    peaks, properties = find_peaks(filtered_intensity, height=200, prominence=50)

    if len(peaks) > 0:
        # Get the index of the highest peak
        max_peak_index = np.argmax(properties['peak_heights'])
        peak_position = filtered_theta.iloc[peaks[max_peak_index]]
        peak_intensity = properties['peak_heights'][max_peak_index]

        # Calculate half maximum
        half_max = peak_intensity / 2

        # Interpolate around the peak to find FWHM
        interp_func = interp1d(filtered_theta, filtered_intensity, kind='linear', bounds_error=False, fill_value=0)
        fine_theta = np.linspace(peak_position - 1, peak_position + 1, 1000)
        fine_intensity = interp_func(fine_theta)
        left_idx = np.where(fine_intensity >= half_max)[0][0]
        right_idx = np.where(fine_intensity >= half_max)[0][-1]

        # Calculate FWHM
        fwhm = fine_theta[right_idx] - fine_theta[left_idx]

        print(f"Highest Peak Position (2θ): {peak_position:.2f}°")
        print(f"Peak Intensity: {peak_intensity:.2f}")
        print(f"FWHM: {fwhm:.2f}°")
    else:
        print("No peaks found in the specified range.")

    # Display crystallinity results
    print(f"Baseline (Amorphous Contribution): {baseline}")
    print(f"Total Area: {total_area:.2f}")
    print(f"Crystalline Area: {crystalline_area:.2f}")
    print(f"% Crystallinity: {percent_crystallinity:.2f}%")

    # Plot the XRD data with the baseline and peaks
    plt.figure(figsize=(10, 6))
    plt.plot(two_theta, intensity, label='Original XRD Data', color='black')
    plt.plot(two_theta, [baseline] * len(two_theta), label='Baseline (Amorphous)', color='red', linestyle='--')
    plt.fill_between(two_theta, baseline, intensity, where=(intensity > baseline), color='green', alpha=0.3,
                     label='Crystalline Area')
    
    # Plot detected peaks as red dots
    if len(peaks) > 0:
        plt.scatter(filtered_theta.iloc[peaks], filtered_intensity.iloc[peaks], color='red', zorder=5, label='Detected Peaks')
        
        # Draw vertical lines at the peak positions
        # for peak in peaks:
        #     plt.axvline(x=filtered_theta.iloc[peak], color='blue', linestyle='--')

        # Display FWHM (Full Width at Half Maximum)
        plt.hlines(y=half_max, xmin=fine_theta[left_idx], xmax=fine_theta[right_idx], color='purple', linestyle='--',
                   label=f'FWHM = {fwhm:.2f}°')

    # Add labels and legends
    plt.title('XRD Data with Crystallinity Analysis and Peak Detection')
    plt.xlabel('2θ (degrees)')
    plt.ylabel('Intensity (a.u.)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save plots
    plt.savefig(output_image)  # Save as image
    plt.savefig(output_pdf)    # Save as PDF
    plt.show()
    print("Processing complete!")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <input_csv_path> <output_image_path> <output_pdf_path>")
    else:
        input_csv = sys.argv[1]
        output_image = sys.argv[2]
        output_pdf = sys.argv[3]
        process_xrd(input_csv, output_image, output_pdf)
