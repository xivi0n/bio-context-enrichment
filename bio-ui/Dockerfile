# Use Node.js 20 LTS as base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Set default environment variables (can be overridden)
ENV VITE_API_BASE_URL=http://localhost:5050
ENV VITE_PORT=5173

# Expose the port (default 5173, but configurable)
EXPOSE $VITE_PORT

# Run the development server with configurable port
CMD ["sh", "-c", "npm run dev -- --port $VITE_PORT"]