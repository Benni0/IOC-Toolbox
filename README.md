# Simple Toolbox for URL tracing

This application provides a simple REST API which is able to get the actual site URL including all called URLs.
You can use this application when you have a link (phishing link, e.g.) and you want to get the actual site URL whitout URL shortening, site protection and redirects.

## SWAGGER
This application uses FastAPI, so SWAGGER is available under `/docs`

## List lookups
This application can also lookup domains in alexa one million and cisco umbrella one million

## Get it running

### Install requirements
This application needs a working Python 3 environment which installed requirements.
A venv can created like this:
``` 
python3 -m venv /path/to/new/virtual/environment
pip install -r /path/to/app/requirements.txt
```

You have to specify an environment variable named API_KEY, which can contain multiple comma seperated strings. One of these strings must be provided in Authorization Header with each request - used for misuse prevention.

### Start the Service
`uvicorn path.to.app.main:app --reload`

### Use Docker
You can also user Docker:
Build the container:
`docker build -t urlservice`

Start the container:
`docker run --env API_KEY=CHANGEME -p 8080:80 urlservice`