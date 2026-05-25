### Accessing APIs With Your Browser

While the output isn't the prettiest, you can easily use your browser to request data from most of our API endpoints.
In particular, you can use any endpoint that supports the "GET" request method.
This includes all endpoints for the File API, which is the API that a human user is most likely to make use of.

To access an API endpoint with your browser, simply perform the following steps:

1. Identify your base URL.
    For example: `ogd-services.fielddaylab.wisc.edu/apis/files/latest/app.wsgi`
2. Identify which endpoint you want to access.
    For example, suppose you want to get the list of datasets for the game AQUALAB.
    The endpoint is: `/games/AQUALAB/datasets`
3. Add the endpoint to the base to get a full URL.
    In our example, this would be:  
    `ogd-services.fielddaylab.wisc.edu/apis/files/latest/app.wsgi/games/AQUALAB/datasets`
4. Open the URL in your browser.
    This step is the same as opening any other URL in your browser.
    You could type it in to the browser's address bar directly, or paste it from somewhere else.
    The result should be a very simple display of some JSON-structured data, corresponding to your request:

    ![The results of an example API request displayed in the Chromium web browser (with pretty-printing enabled)](/assets/images/figures/api-in-browser.png)
