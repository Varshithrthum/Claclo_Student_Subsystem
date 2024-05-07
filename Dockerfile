# Use the official Python image as a base image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Copy the contents of the current directory into the container at /app
COPY . .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 to the outside world
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
