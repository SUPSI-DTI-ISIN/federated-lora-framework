FROM --platform=$TARGETPLATFORM node:22.21-alpine AS builder

ARG NPM_TOKEN
ARG ENV_PATH=.env

WORKDIR /app

RUN echo "@isin:registry=https://gitlab-edu.supsi.ch/api/v4/projects/1401/packages/npm/" > .npmrc
RUN echo "//gitlab-edu.supsi.ch/api/v4/projects/1401/packages/npm/:_authToken=${NPM_TOKEN}" >> .npmrc

COPY package.json .
COPY package-lock.json .
RUN npm ci

RUN rm .npmrc

COPY index.html .
COPY vite.config.ts .
COPY tsconfig*.json ./
COPY src ./src
COPY public ./public
COPY $ENV_PATH .env

RUN npm run build

RUN rm .env

FROM nginx:1.29.4-alpine
COPY --from=builder /app/dist /usr/share/nginx/html

COPY docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY nginx/nginx.conf.template /etc/nginx/templates/

EXPOSE 80
CMD ["/docker-entrypoint.sh"]