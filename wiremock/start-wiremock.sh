#!/bin/bash

echo "Starting NetApp ONTAP Mock Server..."
echo ""
echo "Server will be available at: http://localhost:443"
echo "Admin interface at: http://localhost:443/__admin"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

java -jar wiremock-standalone-3.13.1.jar \
  --port 443 \
  --root-dir . \
  --global-response-templating \
  --verbose
