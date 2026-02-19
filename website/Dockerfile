# Stage 1: Build the static HTML / CSS / JS bundle
#          This stage is responsible for using Jekyll to build the static
#          files that are ultimately served by nginx. This is not the final
#          image.
FROM ruby:3.4.2 AS build-image
ARG http_proxy
ARG https_proxy
ARG no_proxy
ARG TEST_ENV=false

ENV NODE_VERSION=18.17.1
ENV NVM_DIR=/root/.nvm
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
ENV http_proxy=$http_proxy \
    https_proxy=$https_proxy \
    no_proxy=$no_proxy \
    HTTP_PROXY=$http_proxy \
    HTTPS_PROXY=$https_proxy \
    NO_PROXY=$no_proxy

WORKDIR /app
COPY ./website/Gemfile /app/Gemfile
COPY ./website/package.json /app/package.json
RUN apt-get clean && \
    apt-get update && \
    apt-get install -y curl git && \
    apt-get install -y curl git && \
    #command below is needed when ZScaler is active. Will remove before pushing code to main/release.
    # git config --global http.sslVerify false && \
    curl -k -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION} && \
    . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION} && \
    #command below is needed when ZScaler is active. Will remove before pushing code to main/release.
    # npm config set strict-ssl false && \
    npm install --legacy-peer-deps chart.js && \
    bundle install

# Copy prepare-test-files.sh script and cypress directory (needed for test profile)
COPY ./prepare-test-files.sh /prepare-test-files.sh
COPY ./cypress /cypress

# Copy website files
COPY ./website /app

# Conditionally run prepare-test-files.sh
RUN if [ "${TEST_ENV}" = "true" ]; then \
        echo "Test profile detected. Preparing test markdown files..."; \
        chmod +x /prepare-test-files.sh && \
        cd / && \
        TEST_ENV=true /prepare-test-files.sh || echo "Warning: prepare-test-files.sh failed"; \
    else \
        echo "Test profile not active. Skipping test file preparation."; \
    fi

RUN bundle exec jekyll clean && \
    bundle exec jekyll build && \
    npx gulp updateUswds && \
    npx gulp bundleChart

RUN BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") && \
    echo "<!-- Deployment Date: ${BUILD_DATE} -->" >> /app/_site/index.html

# Stage 2: Build the final nginx image
#          This stage is responsible for building the final nginx image that
#          contains the static files generated in Stage 1.
FROM nginxinc/nginx-unprivileged:alpine AS runtime-image
ARG http_proxy
ARG https_proxy
ARG no_proxy

ENV http_proxy=$http_proxy \
    https_proxy=$https_proxy \
    no_proxy=$no_proxy \
    HTTP_PROXY=$http_proxy \
    HTTPS_PROXY=$https_proxy \
    NO_PROXY=$no_proxy
COPY ./website/nginx.conf /etc/nginx/nginx.conf
COPY --from=0 /app/_site /usr/share/nginx/html
EXPOSE 8080