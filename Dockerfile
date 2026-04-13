# Use Maven with Java 21 to build the application
FROM maven:3.9-eclipse-temurin-21 AS build

# Set working directory
WORKDIR /app

# Copy pom.xml and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests

# Use Java 21 runtime for the final image
FROM eclipse-temurin:21-jre

# Set working directory
WORKDIR /app

# Copy the built JAR from build stage
COPY --from=build /app/target/*.jar app.jar

# Expose the application port
EXPOSE 1715

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]

