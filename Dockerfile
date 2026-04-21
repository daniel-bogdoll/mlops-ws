# Use official Python image
FROM python:3.11-slim

# Copy app code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir scikit-learn==1.7.1 flask

# Expose port
EXPOSE 5000

# Run the app
WORKDIR ./serving
CMD ["python", "flask-server_model.py"]
