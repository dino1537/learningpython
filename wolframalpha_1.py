import requests
from rich import print
import matplotlib.pyplot as plt

# Replace 'YOUR_APP_ID' with your actual Wolfram Alpha API key
app_id = 'Your_APP_ID'

# Define the base URL for the Wolfram Alpha API
base_url = 'http://api.wolframalpha.com/v2/query?'

def query_wolfram_alpha(query):
    # Define the parameters for the API request
    params = {
        'input': query,
        'format': 'plaintext',
        'output': 'JSON',
        'appid': app_id
    }

    # Send the HTTP GET request to the API
    response = requests.get(base_url, params=params)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        data = response.json()

        # Extract and format the results
        if 'queryresult' in data and 'pods' in data['queryresult']:
            formatted_output = ""
            for pod in data['queryresult']['pods']:
                if 'title' in pod and 'subpods' in pod:
                    title = pod['title']
                    subpod = pod['subpods'][0]  # Get the first subpod
                    plaintext = subpod['plaintext']
                    formatted_output += f"[bold]{title}[/bold]: {plaintext}\n\n"

            # Print the formatted output
            print(formatted_output)

            # Export as JPEG image
            plt.text(0.1, 0.1, formatted_output, fontsize=12)
            plt.axis('off')
            plt.savefig('output.jpg', bbox_inches='tight')
            plt.close()

            # Export as LaTeX file
            with open('output.tex', 'w') as latex_file:
                latex_file.write(formatted_output)

            # Export as Markdown file
            with open('output.md', 'w') as markdown_file:
                markdown_file.write(formatted_output)

        else:
            print("[italic]No results found.[/italic]\n")

    else:
        print(f"[red]Error:[/red] HTTP Status Code {response.status_code}\n")

if __name__ == '__main__':
    while True:
        # Ask the user for input query
        query = input("Enter your query (or 'exit' to quit): ").strip()
        
        if query.lower() == 'exit':
            break

        # Call the function to query Wolfram Alpha
        query_wolfram_alpha(query)

