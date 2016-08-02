## Omicia API Java Example
This mini project showcases how to interact with the Omicia API using Java.

The project is built against JDK 8, and makes use of Gradle to download dependencies, compile, and run the example. A wrapper for Gradle is included, but Java will need to be available in your environment to run the examples. We are using the Apache HttpComponents library to manage the request/response with the API endpoint.

Additionally, you will need an API key issued by Omicia to make requests. Add these plus your project ID in the [OmiciaApiExample](./src/main/java/com/omicia/examples/OmiciaApiExample.java) file prior to running.

### Running
Run with `./run_example.sh <VCF file>`. This will use Gradle to establish the classpath for running the example. You can also run the example within an IDE that is aware of project dependencies.