import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

def process_csv(input_path, output_image, output_pdf):
    # Read the CSV data
    data = pd.read_csv(input_path)
    
    # Create a plot
    plt.figure(figsize=(10, 6))
    plt.plot(data['x'], data['y'], label="Line")
    plt.xlabel("X-Axis")
    plt.ylabel("Y-Axis")
    plt.title("Sample Plot")
    plt.legend()
    
    # Save the plot as both an image and PDF in the same folder as the script
    plt.savefig(output_image)  # Save as image
    plt.savefig(output_pdf)    # Save as PDF
    
    print("Processing complete!")

if __name__ == "__main__":
    # Get the current directory of the script
    current_directory = os.path.dirname(os.path.realpath(__file__))
    
    # Set the input file path and output file paths in the same directory as the script
    input_path = os.path.join(current_directory, "file.csv")  # Ensure 'file.csv' is in the same directory
    output_image = os.path.join(current_directory, "output_image.png")
    output_pdf = os.path.join(current_directory, "output_file.pdf")
    
    # Call the process function
    process_csv(input_path, output_image, output_pdf)
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
    # Example file paths
    input_path = "../uploads/file-1732572286965-105340181.csv"
    output_image = "../outputs/output_image.png"
    output_pdf = "../outputs/output_file.pdf"
    process_csv(input_path, output_image, output_pdf)
