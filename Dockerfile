# Official Python runtime as a parent image
FROM python:3.9-slim as requirements-stage

# Set the working directory in the container
WORKDIR /tmp

# Build the application - More layering is possible here even for the build stage
FROM requirements-stage as production-stage

RUN mkdir -p /home/app
RUN addgroup --system app && adduser --system --group app

ENV HOME=/home/app
ENV APP_HOME=/home/app/code
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN pip install --upgrade pip
RUN pip install -U setuptools
COPY --from=requirements-stage /tmp/requirements.txt /$APP_HOME/requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Production readiness
EXPOSE 5000
HEALTHCHECK CMD curl --fail http://localhost:5000/health || exit 1

# Run the application using a single worker + ASGI instance
# Single worker is used because AKS will manage the scaling and we wish to avoid conflicts in scaling
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]