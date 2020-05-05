#!/bin/sh

# POST request while without the optional URL
curl \
    --header "Content-Type: application/json" \
    --request POST \
    --data '{"postID":"0", "title":"Testing1", "text":"This is Testing1", "community":"CSUF", "username":"User1"}' \
    http://localhost:5000/api/v1.0/resources/collections


