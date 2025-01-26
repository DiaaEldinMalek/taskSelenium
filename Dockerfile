# Stage 1: Use the official Selenium image with Chrome
FROM selenium/standalone-chrome:latest AS selenium

# Stage 2: Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /taskselenium

# Copy the current directory contents into the container at /taskselenium
COPY . /taskselenium

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir  -r requirements.txt
RUN apt-get update && apt-get install -y wget

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Copy the Selenium server from the first stage
COPY --from=selenium /opt/selenium /opt/selenium

# Set the environment variable to use the Selenium server
ENV PATH="/opt/bin/selenium:${PATH}"


# Run main.py when the container launches
# CMD echo "Running the Selenium script..."
CMD ["python", "main.py", "--to-csv"]