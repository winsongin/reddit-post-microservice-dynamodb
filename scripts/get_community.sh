#!/bin/sh

# GET request that retrieves the N recent posts for a particular community
curl --request GET "http://localhost:5000/api/v1.0/resources/collections/recent?community=CSUF&amount=5"