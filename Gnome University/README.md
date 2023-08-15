We are presented with an S3-hosted page listing some papers from previous year's cloud villages. The filename of the flag is given to us in the description as secret.txt.

http://cloudfilestore.s3-website-eu-west-1.amazonaws.com/

Looking at the source of this page, there are some js functions which interact with a lambda function:

```js
const apiEndpoint = 'https://3k93nsmmy5.execute-api.eu-west-1.amazonaws.com/cloudev1';

// Function to fetch the presigned URL for a file
function fetchPresignedUrl(file, callback) {
    $.ajax({
        url: apiEndpoint + '/download?file_name=' + file + "&storage=research-gnomes-prod",
        type: 'GET',
        success: function(response) {
            console.log('Presigned URL:', response.body.presigned_url.body);
            callback(response.body.presigned_url.body);
        },
        error: function(error) {
            console.error('Error getting presigned URL:', error);
            callback(null); // Call the callback with null in case of an error
        }
    });
}
```

The API call in fetchPresignedUrl takes a bucket name in the storage parameter. It's hardcoded in the function, but if we call it for `secret.txt`, we get a KeyError, which tells us that the file we're looking for isn't there. If we switch "research-gnomes-prod" for "research-gnomes-dev" and make our call, we get back a signed url, which takes us to the flag.
