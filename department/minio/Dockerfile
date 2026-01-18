FROM alpine:3.19

RUN apk update
RUN apk add --no-cache curl bash \
 && curl -sSL https://dl.min.io/client/mc/release/linux-amd64/mc \
    -o /usr/bin/mc \
 && chmod +x /usr/bin/mc

WORKDIR /app

COPY setup_minio.sh /app/setup_minio.sh
RUN chmod +x /app/setup_minio.sh

CMD ["/bin/sh", "/app/setup_minio.sh"]