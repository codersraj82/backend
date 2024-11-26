# Step 1: Use the official Python image
FROM python:3.11-slim

# Step 2: Install Node.js and system dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy your project files into the container
COPY . .

# Step 5: Create and activate a Python virtual environment
RUN python3 -m venv venv

# Step 6: Upgrade pip and install Python dependencies
RUN ./venv/bin/pip install --upgrade pip
RUN ./venv/bin/pip install -r requirements.txt

# Step 7: Install Node.js dependencies
RUN npm install

# Step 8: Expose the necessary port (e.g., 3000 for your Node.js server)
EXPOSE 3000

# Step 9: Set the default command to run the Node.js server
CMD ["node", "index.js"]
