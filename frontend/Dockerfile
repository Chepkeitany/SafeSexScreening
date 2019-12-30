# base image
FROM node:12.2.0-alpine as builder

# set working directory
RUN mkdir -p /app

WORKDIR /app

COPY . /app

# build React app and install dependencies
RUN yarn
RUN yarn build

# deploy to NGINX
FROM nginx

COPY --from=builder /app/build /usr/share/nginx/html/
COPY --from=builder /app/build /usr/share/nginx/html/ss2frontend/
COPY --from=builder /app/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
