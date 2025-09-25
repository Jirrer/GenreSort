# Stage 1: Build Vite app
FROM node:20 AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci
COPY . .

# Build arg for backend URL
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL:-http://backend:5000}

RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:stable-alpine
RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
