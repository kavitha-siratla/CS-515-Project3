#!/bin/sh

set -e # exit immediately if newman complains
trap 'kill $PID' # kill the server on exit

./run.sh &&
PID=$1 # record the PID

newman run forum_multiple_posts.postman_collection.json -e env.json # use the env file
newman run forum_post_read_delete.postman_collection.json -n 50 # 50 iterations