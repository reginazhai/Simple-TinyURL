// Get the long url from the form

// Reference: https://stackoverflow.com/questions/11563638/how-do-i-get-the-value-of-text-input-field-using-javascript
function submitData(event) {
    event.preventDefault();
    const long_url = document.getElementById('url').value;
    shortenUrl(long_url);
}

// Reference: https://www.freecodecamp.org/news/make-api-calls-in-javascript/#how-to-make-post-requests
function shortenUrl(url) {
    const api_request = {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({url: url})};

    // Send the long url to the backend API for shortening
    fetch('/shorten', api_request)
    .then(response => {if (!response.ok) {
        throw new Error("Error: " + response.status + ' ' + response.statusText);
      }
      return response.json();
    })
    .then(data => {
        document.getElementById('result').innerHTML = "<p>Shortened URL: " + data.shortened_url + "</p>";
    })
    .catch(error => console.error('Error:', error));
}
