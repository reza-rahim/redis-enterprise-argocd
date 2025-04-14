# Use Alpine as base image
FROM alpine

# Install dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    curl \
    openssl \
    kubectl \
    jq


# Create a virtualenv and install tools in it
RUN python3 -m venv /opt/venv \
 && . /opt/venv/bin/activate \
 && pip install awscli redis flask


# Set PATH so commands like aws and python work globally
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN adduser -D appuser
USER appuser
WORKDIR /home/appuser
