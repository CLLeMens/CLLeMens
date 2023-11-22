#!/bin/sh

# Start localtunnel
lt --port 8000 > url.txt &

# Wait for the URL to be generated
sleep 10

# Extract the URL
URL=$(cat url.txt | grep -o 'https://[^ ]*')
