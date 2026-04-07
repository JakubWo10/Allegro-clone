FROM node:20-slim

WORKDIR /app/frontend

COPY .env_docker_compose ../

COPY frontend/package*.json ./

RUN npm install

COPY frontend/ .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
