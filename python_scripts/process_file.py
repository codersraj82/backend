import sys
import pandas as pd
import matplotlib.pyplot as plt

def process_csv(input_path, output_image, output_pdf):
    data = pd.read_csv(input_path)
    plt.figure(figsize=(10, 6))
    plt.plot(data['x'], data['y'], label="Line")
    plt.xlabel("X-Axis")
    plt.ylabel("Y-Axis")
    plt.title("Sample Plot")
    plt.legend()
    plt.savefig(output_image)  # Save as image
    plt.savefig(output_pdf)    # Save as PDF
    print("Processing complete!")

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_image = sys.argv[2]
    output_pdf = sys.argv[3]
    process_csv(input_path, output_image, output_pdf)
