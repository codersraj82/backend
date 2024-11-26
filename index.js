const { PythonShell } = require("python-shell");

// Specify the Python executable explicitly
PythonShell.defaultOptions = {
  pythonPath: "/usr/local/bin/python", // Adjust this to the correct path of your Python executable
  pythonOptions: ["-u"], // Optional: unbuffered output for real-time output
};

// Run a Python script to check if pandas is installed
const options = {
  args: [], // No arguments needed for the check
};

PythonShell.runString(
  `
try:
    import pandas as pd
    print("Pandas is installed, version:", pd.__version__)
except ImportError:
    print("Error: pandas is not installed")
  `,
  options,
  function (err, result) {
    if (err) {
      console.error("PythonShell error:", err);
    } else {
      console.log("Python output:", result);
    }
  }
);
