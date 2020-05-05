#!/bin/sh

# POST request with the optional URL included
curl \
    --header "Content-Type: application/json" \
    --request POST \
    --data '{"postID":"1", "title":"Testing2", "text":"This is Testing2", "community":"CompSci", "url":"http://fullerton.edu", "username":"User2"}' \
    http://localhost:5000/api/v1.0/resources/collections