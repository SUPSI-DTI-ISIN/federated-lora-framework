FROM --platform=$TARGETPLATFORM node:22.21-alpine AS builder

ARG ENV_PATH=.env

WORKDIR /app

COPY package.json .
COPY package-lock.json .
RUN npm ci

COPY index.html .
COPY vite.config.ts .
COPY tsconfig*.json ./
COPY src ./src
COPY public ./public
COPY $ENV_PATH .env

RUN npm run build

FROM nginx:1.29.4-alpine
COPY --from=builder /app/dist /usr/share/nginx/html

COPY docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY nginx/nginx.conf.template /etc/nginx/templates/

EXPOSE 80
CMD ["/docker-entrypoint.sh"]