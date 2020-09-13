# Instructions for Docker for building the Munch API image
# Use the official Python image to start with
FROM python:3
# Setup the working directory for the application
WORKDIR /usr/src/app
# Copy the requriements.txt file
COPY requirements.txt ./
# Install the dependencies mentioned in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Copy the application code
COPY . .
# Expose at port 5000
EXPOSE 5000
# Start Python and run the script when the container is up
ENTRYPOINT [ "python" ]
CMD [ "./app/api.py" ]