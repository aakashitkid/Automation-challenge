# Use official Python image
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && \
    apt-get install -y wget gnupg libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libgbm1 libxshmfence1 libxcomposite1 libxdamage1 libxrandr2 libxinerama1 libpango-1.0-0 libpangocairo-1.0-0 libatk1.0-0 libcups2 libdrm2 libx11-xcb1 && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN pip install playwright && playwright install --with-deps

# Copy the rest of the code
COPY . .

# Run containerized tests in headless mode by default
ENV HEADLESS=1

# Default command (can be overridden)
CMD ["pytest", "-s", "tests/assignment1.py"]
