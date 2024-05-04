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

### URL Shortening Service

Here, we provide:

- An API endpoint to receive a long URL and return a shortened URL.
  - We created the API endpoint at `/shorten` that receives the long URL through `POST` method and returns the JSON version of the shortened URL.
  - The input and output are interacted through frontend at `/`.
- A mechanism to store the mappings between original URLs and their corresponding shortened versions
efficiently.
  - See details in [Database Selection](#database-selection) and [Short URL Generation Algorithm](#short-url-generation-algorithm).
- Handling of edge cases such as invalid URLs or duplicate requests.
  - Given the complexity of the composition of URLs, and that links emerge and die from time to time, we cannot really know if a URL is valid unless we try to open it. But considering the time it takes to verify one website, here I using a simpler check from `urllib.parse`. The reference for the code is from [StackOverflow](https://stackoverflow.com/questions/25259134/how-can-i-check-whether-a-url-is-valid-using-urlparse).
  - Duplicate requests are handled through checking mechanism before inserting into database.
- Redirection mechanism to forward users to the original URL when they access the shortened URL.
  - We created the redirection endpoint at `/<short_url>`, which decodes the short_url to the corresponding ID, then retrieve the original URL and redirect to the original URL. 

### Database Selection 

Assuming we are only running the service of shortening the URL, it is less likely that we will need more types of schemas, which is the main benefit of NoSQL databases. Therefore, RDBMS with SQL would be sufficient for storing the mappings between original URLs and their corresponding shortened versions.

SQLite is a light-weight data engine that is integrated nicely with Python, which is the language that we are using for backend. For the purpose of a demo application, SQLite should be able to handle the service. However, when the service expand and we need to consider high traffic volumns and handling requests in parellel, SQLite is not the best option, and we could possibly change to MySQL or PostgreSQL, which allows for higher throughput, better concurrency and better scalability.

### Short URL Generation Algorithm

First, we would like to decide how many digits we are generating for the short URL. Suppose we decided to have $n$ digits for the shortened URL. Given that we can use characters from [0-9][a-z][A-Z], we will have $62^n$ possible URLs that we can generate. Depending on the service size, we can choose $n$ differently. We are now using $n=6$ for simplicity since $62^6 = 56,800,235,584$, which is sufficient for a smaller service.

There are several popular options for the algorithm design of short URL generation. All of them have pros and cons, and the detailed implementation for the system should also be dependent on the details of the services.

1. Random string generation
   
   As stated, the first algorithm is generating random strings as replacement of the long URL
   - Pros: 
     - Secure: if we assume the strings are generated through completely random generator, then hard to decode based on the short URL.
     - Scalable: easy to generate the URL even with high concurrency and distributed systems.
   - Cons:
     - Collision: the possiblity of URLs colliding will increase as the number of URLs stored increase. The handling of collision will require extra time and calculation. (But can be mitigated when increasing the number of digits for shortened URLs)
2. Hashing algorithms
   
   There are common secure hashing algorithms (such as MD5 and SHA-256) that can be used to generate the shortened URL links by manipulating the outputs from the hashing algorithms. 
   - Pros:
     - Secure: will not be able to decode the original URL
     - Scalable: can be easily generated in larger scale
   - Cons:
     - Possible collision: depending on how we convert the outputs from hashing algorithms to the $n$ bits that we want, we might have collision issues.
3. BaseX encoding (X being an integer)
   
   Given that we will have be storing the URLs in the database, there will be an id that keeps track of the order of the URLs saved in the system. We can convert the number into BaseX encoding through base conversion.
   - Pros:
     - No collisions: since the order is distinct, we will not have any collisions in the shortened URLs.
     - Secure: secure in the sense that the original URL cannot be easily guessed through the output URL. 
   - Cons:
     - Limited scalability: the order has to be obtained by accessing the database, which can be hard when the traffic is high or when the system is distributed. 
4. Combination of the above
   
   There are also other possible algorithms that tries to balance the above pros and cons by combining them. But one potential problem would be that combining the above methods makes it more complex to calculate and thus require more time for each URL generation.
5. Other algorithms
   
   There are also other algorithms that aims to make the URL more human-readable by providing shortened URLs with details related to the actual content of the website. 

For the simplicity and limitation of the project, we are using Base62 encoding to avoid potential time required for collision detection. In this case, we do not need to store the shortened URL (as the short URL is directly converted from the id). 

### Frontend Design

The frontend design is simple, with the title and the main interface to input. The input is taken as a form that receives the long URL, and connects to the API endpoint that handles the backend calculation through `POST` method. When a response is returned from the API endpoint, we receive the link and display it at the webpage. The link can also be clicked so that the user can be redirected directly to the original URL. It is also a way of testing if the system works.

### Further improvements

The current error handling is present but not very informative to the user. So a possible improvement on this would be to redirect to webpages (or sends out alerts) that displays the error to the user for improved inputs.

## Additional Considerations

### Security

- Implement measures to prevent abuse of the URL shortening service, such as rate limiting and validation of input URLs.
  - Rate limiting is implemented through Flask limiter and adjustable based on application. The reference for the code is on [Medium](https://medium.com/analytics-vidhya/how-to-rate-limit-routes-in-flask-61c6c791961b).
  - We validate the input URLs through a simpler check from `urllib.parse`. The reference for the code is from [StackOverflow](https://stackoverflow.com/questions/25259134/how-can-i-check-whether-a-url-is-valid-using-urlparse).
- Discuss strategies to protect shortened URLs from being guessed or brute-forced.
  -  See more details in [Short URL Generation Algorithm](#short-url-generation-algorithm).

### Scalability:
- Consider how your system would scale to handle a large number of URL shortening requests and high traffic volumes.
  - See more details in [Short URL Generation Algorithm](#short-url-generation-algorithm).

### Testing
- Describe your approach to testing both the backend and frontend components. Include unit tests, integration tests, and end-to-end tests where applicable.
  - Given the time and capacity constraints, tests are performed as the code is developed. Since the code is developed by breaking down into subfunctions, testing is also done by functionality.
  - Backend Tests:
    - Backends are tested through individual functions. While I did not write out unittest code, tests on Base62 encoding and decoding, on URL shortening and dataset queries are tested under different scenarios with both valid and invalid inputs to satisfy the required restrictions and error handling.
  - Frontend Tests:
    - Frontend tests are conducted on the browser to interact with the functionalities of the JavaScript. Styles are inspected also on the browser.
  - End-to-end tests:
    - Most of the tests are performed end-to-end to test functionality of the URL shortening service and the redirection.

### Deployment
- Discuss how you would deploy the system to production, including considerations for scalability, reliability, and monitoring.
  - Now that we have a basic version of the tiny-url system, we need to consider the option of deployment. There are quite a few factors to consider:
    - The current version of the code is based on the assumption that we will be hosting a small platform and will not handle high traffic and too much concurrency. Based on the goal of the service, we will need to change some of the design decisions and modify the code to align better with the need of the user and the real world scenario. 
    - After making the adjustments, before actually deploying, we still need to add more rigorous testing on various cases to make sure that the software functions as intended and as reliable as we can provide. 
    - After deploying, we need to find ways to monitor and improve the deployed system. Tools are available along with the deployment to monitor the performance of the application as well as the rate and user status. We need to properly define and setup anomaly detection in the monitor tools to send out alerts when strange things happen.
    - In the unfortunate case of a crash, we need to consider having backups for both the system and the database. These backups will also need to checked regularly in case of emergency. 