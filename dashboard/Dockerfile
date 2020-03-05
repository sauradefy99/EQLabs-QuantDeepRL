FROM node:alpine as build

COPY package.json /package.json
COPY package-lock.json /package-lock.json

RUN npm install

FROM node:alpine

COPY --from=build /* /
COPY --from=build /node_modules /node_modules
COPY ./src /src
COPY ./public /public

CMD ["npm", "start"]
