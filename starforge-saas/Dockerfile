# --- Build Stage ---
FROM node:20-alpine AS build-assets

WORKDIR /app

# Copy package files and install deps
COPY package.json package-lock.json* ./
RUN npm ci

# Copy app static assets and Tailwind config
COPY app/static ./app/static
COPY tailwind.config.js postcss.config.js ./

# Build CSS and JS bundles
RUN npm run build

# --- Final Stage ---
FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask app code
COPY app ./app
COPY run.py ./

# Copy built static assets from build stage
COPY --from=build-assets /app/app/static ./app/static

# Expose Flask port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
