FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the application files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.python.org/simple

# Expose the port the app runs on
EXPOSE 5004

# Optional: copy your .env file (if you want it inside container)
COPY .env .env

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5004

# Run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5004", "main:app"]
