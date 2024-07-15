FROM node:18-bookworm
WORKDIR /frontend-app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 4173
CMD [ "npm", "run", "preview" ]