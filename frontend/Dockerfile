FROM node:24-alpine AS build
WORKDIR /build

# O lockfile entra antes do codigo: dependencias mudam menos que telas, e o
# cache do Docker so serve se a camada estavel vier primeiro.
COPY package.json package-lock.json* ./
RUN npm ci --no-audit --no-fund

COPY tsconfig.json vite.config.ts index.html ./
COPY src ./src
RUN npm run build

FROM nginx:1.29-alpine AS runtime
COPY --from=build /build/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
