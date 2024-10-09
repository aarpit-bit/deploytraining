# Use Python 3.11.5 as the base image
FROM python:3.11.5

# Set the working directory in the container
WORKDIR app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the Flask server when the container launches
CMD ["python", "-u", "app.py"]

