import requests

import os
from utils.io import load_json

# Set the API key
curr_filepath = os.path.dirname(os.path.abspath(__file__))
curr_dirname = os.path.dirname(curr_filepath)
filename=os.path.join(curr_dirname, "secrets/youtube_api.json")
print(filename)
assert os.path.exists(filename), "Please create a file with your youtube api key"


# API_KEY = load_json(filename)["api_key"]

# # Set the parameters for the search query
# params = {
#     "part": "snippet",
#     "publishedAfter": "2021-12-01T00:00:00Z",  # Videos published after December 1, 2021
#     "key": API_KEY
# }

# # Make the request to the search.list method of the YouTube Data API
# response = requests.get(
#     "https://www.googleapis.com/youtube/v3/search",
#     params=params
# )

# import ipdb; ipdb.set_trace()

# # Print the response
# print(response.json())

import requests

# Set the API key
API_KEY = load_json(filename)["api_key"]

# Set the parameters for the search query
params = {
    "part": "snippet",
    "publishedAfter": "2021-12-01T00:00:00Z",  # Videos published after December 1, 2021
    "key": API_KEY,
    "maxResults": 5,  # Set the maximum number of results per page to 5
    "pageToken": ""  # Initialize the page token to an empty string
}

# Initialize an empty list to store the results
results = []

# Loop until there are no more pages of results
condition = True
condition = len(results) < 100  # Set the condition to stop the loop
while condition:
    # Make the request to the search.list method of the YouTube Data API
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/search",
        params=params
    )
    response_json = response.json()

    # Add the results from the current page to the list of results
    try:
        results.extend(response_json["items"])
    except:
        import ipdb; ipdb.set_trace()

    # Check if there is a next page of results
    if "nextPageToken" in response_json:
        # Set the page token for the next page of results
        params["pageToken"] = response_json["nextPageToken"]
    else:
        # There are no more pages of results, so break the loop
        break

# Print the list of results
import ipdb; ipdb.set_trace()
print(results)
