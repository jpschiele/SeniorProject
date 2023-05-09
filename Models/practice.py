import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

# List of school names to scrape data for
schools = ['baylor', 'duke', 'kentucky']

for school in schools:
    # URL of the web page to scrape
    url = f'https://www.sports-reference.com/cbb/schools/{school}/men/2022-gamelogs.html'
    print('1')

    # Send a GET request to the URL
    response = requests.get(url)
    print('2')

    # Use Beautiful Soup to parse the HTML content of the response
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)

    # Find the table containing the game log information
    table = soup.find('table', {'id': 'sgl-basic_NCAAM'})
    print('4')

    # Use Pandas to read the HTML table into a DataFrame
    df = pd.read_html(str(table))[0]
    print('5')

    # Replace empty strings with NaN values
    df.replace('', np.nan, inplace=True)
    print('6')

    # Drop any rows with missing data
    df.dropna(inplace=True)
    print('7')

    # Write the data to a CSV file
    filename = f'C:/Users/jpsch/OneDrive/Documents/SeniorProject/{school}_game_log.csv'
    df.to_csv(filename, index=False)
    print('8')
