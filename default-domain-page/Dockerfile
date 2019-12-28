FROM node
WORKDIR /app
COPY package.json .
COPY yarn.lock .
RUN yarn
COPY . .
RUN yarn build
CMD ["yarn", "start", "-H", "0.0.0.0", "-p", "80"]
EXPOSE 80
