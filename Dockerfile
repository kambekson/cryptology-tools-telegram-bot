# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Set environment variables (optional, for example if you use .env)
# ENV API_TOKEN=your_token
# ENV API_SERVER=your_server

# Run the bot
CMD ["python", "main.py"]