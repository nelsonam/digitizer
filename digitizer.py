import httplib, urllib, base64, time, json

# Keys
endpoint = 'westcentralus.api.cognitive.microsoft.com'
api_key = 'TEST_KEY'


headers = {
    # Request headers.
    # Another valid content type is "application/octet-stream".
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': api_key,
}

# The URL of a JPEG image containing handwritten text.
body = "{'url':'http://i.imgur.com/W2fF6uC.jpg'}"

# For printed text, set "handwriting" to false.
params = urllib.urlencode({'handwriting' : 'true'})

try:
    # This operation requrires two REST API calls. One to submit the image for processing,
    # the other to retrieve the text found in the image.
    #
    # This executes the first REST API call and gets the response.
    conn = httplib.HTTPSConnection(endpoint)
    conn.request("POST", "/vision/v1.0/RecognizeText?%s" % params, body, headers)
    response = conn.getresponse()

    # Success is indicated by a status of 202.
    if response.status != 202:
        # Display JSON data and exit if the first REST API call was not successful.
        parsed = json.loads(response.read())
        print ("Error:")
        print (json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()
        exit()

    # The 'Operation-Location' in the response contains the URI to retrieve the recognized text.
    operationLocation = response.getheader('Operation-Location')
    parsedLocation = operationLocation.split(endpoint)
    answerURL = parsedLocation[1]

    # NOTE: The response may not be immediately available. Handwriting recognition is an
    # async operation that can take a variable amount of time depending on the length
    # of the text you want to recognize. You may need to wait or retry this GET operation.

    print('\nHandwritten text submitted. Waiting 10 seconds to retrieve the recognized text.\n')
    time.sleep(10)

    # Execute the second REST API call and get the response.
    conn = httplib.HTTPSConnection(endpoint)
    conn.request("GET", answerURL, '', headers)
    response = conn.getresponse()
    data = response.read()

    # 'data' contains the JSON data. The following formats the JSON data for display.
    parsed = json.loads(data)
    print ("Response:")
    print (json.dumps(parsed, sort_keys=True, indent=2))
    lines = parsed['recognitionResult']['lines']
    for line in reversed(lines):
        print line['text']

    conn.close()

except Exception as e:
    print('Error:')
    print(e)
