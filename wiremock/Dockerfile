# Use Java 11 runtime for WireMock
FROM eclipse-temurin:11-jre-alpine

# Set working directory
WORKDIR /wiremock

# Copy WireMock standalone JAR
COPY wiremock-standalone-3.13.1.jar .

# Copy mappings and response files
COPY mappings/ ./mappings/
COPY __files/ ./__files/

# Expose WireMock port
EXPOSE 443

# Run WireMock with configuration
ENTRYPOINT ["java", "-jar", "wiremock-standalone-3.13.1.jar"]
CMD ["--port", "443", "--root-dir", ".", "--global-response-templating", "--verbose"]

