#!/bin/sh

# DELETE request that deletes the row with postID=0 and community=CSUF
curl --request DELETE "http://localhost:5000/api/v1.0/resources/collections?postID=0&community=CSUF"