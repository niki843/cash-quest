# Use the latest Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the FastAPI application code
COPY /app/ .

# Copy dependencies file
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# load the data from
RUN python download_data.py

# Expose the FastAPI default port
EXPOSE 8000

# Run the FastAPI application
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
