import requests
from bs4 import BeautifulSoup
from rich import print

# Define the URL of the espncricinfo page
url = "https://www.espncricinfo.com/live-cricket-score"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find and extract the cricket scores
    score_divs = soup.find_all("div", class_="match-score-block")

    # Create a list to store the formatted scores
    formatted_scores = []

    # Iterate through the score_divs and format the scores
    for i, score_div in enumerate(score_divs, 1):
        match_title = score_div.find("span", class_="match-title").text.strip()
        score = score_div.find("span", class_="score").text.strip()

        formatted_score = f"[bold]{i}. {match_title}[/bold]: [green]{score}[/green]"
        formatted_scores.append(formatted_score)

    # Print the formatted scores using rich
    if formatted_scores:
        print("\n".join(formatted_scores))
    else:
        print("[red]No live cricket scores found.[/red]")
else:
    print("[red]Failed to retrieve the page.[/red]")

