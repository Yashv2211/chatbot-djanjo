
# Application Setup and Usage Guide

This guide provides detailed steps on setting up and running the Python application within a virtual environment. Follow these instructions to ensure the application operates correctly.

## Setting Up the Virtual Environment

Before running the application, you must activate the Python virtual environment. This environment has all the necessary dependencies installed. To activate the virtual environment, navigate to the project directory and run the following command:

\```bash
source ../env/bin/activate
\```

This command assumes that you are currently in the application directory and that the virtual environment is located in the parent directory under \`env/bin/\`.

## Starting the Application

Once the virtual environment is activated, you can start the application server by using the \`manage.py\` script included in the project. Replace \`<PORT>\` with the actual port number where you want the application to listen for requests. For example, to start the server on port 8080, run:

\```bash
python manage.py runserver <PORT>
\```

## API Endpoint

The application features an API listening on the \`/prompt\` endpoint. You can access the API through the following URL, substituting \`8080\` with your chosen port number if different:

\```
http://127.0.0.1:8080/prompt
\``

### API Request Format

The API expects a POST request with a JSON body containing the following structure:

\```json
{
    "username": "<USERNAME>",
    "prompt": "<PROMPT>"
}
\```

Replace \`<USERNAME>\` and \`<PROMPT>\` with the actual username and the prompt text, respectively. Both fields are required and should be of type string.

## Running Tests

To ensure that the application functions correctly, you can run tests using the following command:

\```bash
python manage.py test chatbotDemo.test.test_views
\```

This command will run all tests written for the views in the \`chatbotDemo\` application, helping you verify that the API handles requests and errors as expected.

## Required Environment Variables

The application requires the following environment variables to be set in the \`.env\` file located in the project directory:

- \`PINECONE_API_KEY\`: Your Pinecone API key.
- \`PINECONE_INDEX\`: The Pinecone index name.
- \`INDEX_DIMENSIONS\`: The dimensions for the Pinecone index.
- \`OPENAI_API_KEY\`: Your OpenAI API key.

Ensure these variables are set correctly to enable all features of the application.

---

Follow these instructions carefully to avoid issues with application setup and API interaction. If you encounter any problems, verify that the virtual environment is activated and that the server is running on the correct port. Also, ensure that all required environment variables are configured correctly.
