# Simple-TinyURL
This is a simple implementation of TinyURL system using Python, SQLite for backend and HTML, CSS and JavaScript for front-end.

## Setup

1. Clone the git repository
```
git clone https://github.com/reginazhai/Simple-TinyURL.git
cd Simple-TinyURL
```

2. Create & activate conda environment with python version 3.8
```
conda create --name tinyurl python=3.8
conda activate tinyurl
```

3. Install the required packages in `requirements.txt`
```
pip install -r requirements.txt
```

## Running Application Locally

1. Run the Flask application
```
python app.py
```
2. Once the server is setup and running correctly, open the web browser and navigate to `http://127.0.0.1:5000`.

## Design Decisions

### Database Selection

### 

## Additional Considerations

### Security

- Implement measures to prevent abuse of the URL shortening service, such as rate limiting and validation of input URLs.
- Discuss strategies to protect shortened URLs from being guessed or brute-forced. 

### Scalability:
- Consider how your system would scale to handle a large number of URL shortening requests and high traffic volumes.

### Testing
- Describe your approach to testing both the backend and frontend components. Include unit tests, integration tests, and end-to-end tests where applicable.
### Deployment
- Discuss how you would deploy the system to production, including considerations for scalability, reliability, and monitoring.


## References
