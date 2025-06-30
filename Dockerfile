# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy source code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir 

# Expose the port Cloud Run expects
EXPOSE 8080

# Command to run the app
CMD ["python", "app.py"]
