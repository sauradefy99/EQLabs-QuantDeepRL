FROM node:alpine as executor_builder

COPY ./package.json /home/node/app/package.json
COPY ./package-lock.json /home/node/app/package-lock.json

WORKDIR /home/node/app

RUN npm install

FROM node:alpine

COPY --from=executor_builder /home/node/app/node_modules /home/node/app/node_modules
ADD ./lib.js /home/node/app/lib.js
ADD ./index.js /home/node/app/index.js

WORKDIR /home/node/app

CMD ["node", "index.js"]
