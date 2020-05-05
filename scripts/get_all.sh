#!/bin/sh

# GET request that retrieves the N recent posts from any community
curl --request GET "http://localhost:5000/api/v1.0/resources/collections/any?amount=2"