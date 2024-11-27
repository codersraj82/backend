import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import simps

# Load your XRD data
file_path = r"E:\Knime\Knime software\XRD\XRD of iron oxide\FeO3-A-converted-modified-renamed.csv"

# Read the CSV file
data = pd.read_csv(file_path)

# Extract 2-theta and intensity
two_theta = data['2theta']
intensity = data['Intensity (a.u)']

# Baseline correction (amorphous background estimation)
# This can be refined using advanced fitting techniques
baseline = np.min(intensity)

# Subtract baseline from the intensity
corrected_intensity = intensity - baseline

# Integrate total area (crystalline + amorphous)
total_area = simps(intensity, two_theta)

# Integrate crystalline area (above the baseline)
crystalline_area = simps(corrected_intensity, two_theta)

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
plt.fill_between(two_theta, baseline, intensity, where=(intensity > baseline), color='green', alpha=0.3, label='Crystalline Area')
plt.title('XRD Data with Crystallinity Analysis')
plt.xlabel('2θ (degrees)')
plt.ylabel('Intensity (a.u)')
plt.legend()
plt.grid()
plt.show()