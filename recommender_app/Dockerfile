# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8501 to the outside world
EXPOSE 8501

# Run streamlit when the container launches
# Using shell form to allow variable expansion if needed, though specific port 8501 is exposed above.
# Railway usually injects PORT, but Streamlit default is 8501. 
# We'll use sh -c to be flexible with PORT env var if provided, defaulting to 8501.
CMD ["sh", "-c", "streamlit run streamlit.py --server.port=$PORT --server.address=0.0.0.0"]

