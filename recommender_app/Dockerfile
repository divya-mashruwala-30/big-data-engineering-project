# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for FAISS
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install CPU-only PyTorch first (to save space and build time)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8501 to the outside world
EXPOSE 8501

# Run streamlit when the container launches
# Railway injects PORT env var - use it with fallback to 8080
CMD ["sh", "-c", "streamlit run streamlit.py --server.port=${PORT:-8080} --server.address=0.0.0.0"]

