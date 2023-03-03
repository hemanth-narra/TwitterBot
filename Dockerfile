# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Install Firefox and Geckodriver
RUN apt-get update && apt-get install -y firefox-esr && \
    apt-get install -y curl && \
    export GECKODRIVER_VERSION='v0.32.2' && \
    curl -L -O https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -xvzf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin/ && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python3", "bot.py"]
