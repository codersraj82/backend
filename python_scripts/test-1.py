import sys
print("Python version")
print(sys.version)
print(sys.executable)
try:
    import pandas as pd
    print("Pandas is installed, version:", pd.__version__)
except ImportError:
    print("Error: pandas is not installed")