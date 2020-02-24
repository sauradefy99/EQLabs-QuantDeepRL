FROM node:alpine as builder

COPY ../lib/package.json /home/node/app/package.json
COPY ../lib/package-lock.json /home/node/app/package-lock.json

WORKDIR /home/node/app

RUN npm install

FROM node:alpine as production

COPY --from=builder /home/node/app/node_modules /home/node/app/node_modules
ADD index.js /home/node/app/index.js

WORKDIR /home/node/app

CMD ["node", "index.js"]
