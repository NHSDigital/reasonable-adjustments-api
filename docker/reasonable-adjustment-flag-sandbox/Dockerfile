FROM node:20.0.0-alpine3.16

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY src ./src

EXPOSE 9000
ENTRYPOINT ["npm", "start"]
