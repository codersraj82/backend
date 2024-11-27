import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from scipy.integrate import simps
from numpy import trapz

def process_xrd(file_path, output_image, output_pdf):
    # Load the XRD data
    data = pd.read_csv(file_path)
     # Read the CSV file
    xrd_data = pd.read_csv(file_path, header=0)

    # Strip spaces from column names
    xrd_data.columns = xrd_data.columns.str.strip()

    # Check if required columns are present
    if '2theta' not in data.columns or 'Intensity (a.u)' not in data.columns:
        print("Error: Missing required columns ('2theta', 'Intensity (a.u)') in the CSV file.")
        return

    # Extract 2-theta and intensity
    two_theta = data['2theta']
    intensity = data['Intensity (a.u)']

    # Baseline correction (amorphous background estimation)
    baseline = np.min(intensity)

    # Subtract baseline from the intensity
    corrected_intensity = intensity - baseline

    # Integrate total area (crystalline + amorphous)
    # total_area = simps(intensity, two_theta)
    total_area = trapz(intensity, two_theta)

    # Integrate crystalline area (above the baseline)
    # crystalline_area = simps(corrected_intensity, two_theta)
    crystalline_area = trapz(corrected_intensity, two_theta)

    # Calculate % Crystallinity
    percent_crystallinity = (crystalline_area / total_area) * 100

    # Display the results
    print(f"Baseline (Amorphous Contribution): {baseline}")
    print(f"Total Area: {total_area:.2f}")
    print(f"Crystalline Area: {crystalline_area:.2f}")
    print(f"% Crystallinity: {percent_crystallinity:.2f}%")

    # Plot the XRD data with the baseline
    plt.figure(figsize=(10, 6))
    plt.plot(two_theta, intensity, label='Original XRD Data', color='black')
    plt.plot(two_theta, [baseline] * len(two_theta), label='Baseline (Amorphous)', color='red', linestyle='--')
    plt.fill_between(two_theta, baseline, intensity, where=(intensity > baseline), color='green', alpha=0.3,
                     label='Crystalline Area')
    plt.title('XRD Data with Crystallinity Analysis')
    plt.xlabel('2θ (degrees)')
    plt.ylabel('Intensity (a.u)')
    plt.legend()
    plt.grid()
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
