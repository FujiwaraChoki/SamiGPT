from PyHostr import PyHostr
import openai
import json

api_key = open('key.txt', 'r').read().strip()

def generate_text(prompt):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt["prompt"],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    print(response.choices[0].text)

    return {
        "response": response.choices[0].text
    }

server = PyHostr("localhost", 9000)

# Creating a GET route
server.get(route="/", response_headers={"Content-type": "text/html"},
            response="At home!")

# Creating a POST route
server.post(
    route="/generate", response_headers={
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
        }, handler=generate_text)

# Finally, start the server
server.serve()