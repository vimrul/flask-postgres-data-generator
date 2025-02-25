# Use official Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask psycopg2 faker gunicorn

# Expose port 5000 for Flask
EXPOSE 5000

# Run the Flask application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
