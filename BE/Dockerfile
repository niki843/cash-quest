# Use the latest Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy dependencies file
COPY . requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# load the data from
RUN python app/download_data.py

# Copy the FastAPI application code
COPY . .

# Expose the FastAPI default port
EXPOSE 8000

# Run the FastAPI application
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
