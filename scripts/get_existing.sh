#!/bin/sh

# GET request that retrieves an existing post using the postID and community as arguments
curl --request GET "http://localhost:5000/api/v1.0/resources/collections?postID=0&community=CSUF"