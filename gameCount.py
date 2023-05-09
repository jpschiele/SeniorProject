from confTeams import get_teams
from firestoreClient import client_setup

# gameCount.py is used for testing to make sure there are an equal number of wins and losses within each conference
# for each year in the database. This means all games are included and all stats are counted for each team.

# Creates connection to Firestore Database
db = client_setup()

# List of conferences
conferences = ['ACC', 'Big10', 'Big12', 'BigEast', 'PAC12', 'SEC']

# Print out wins and losses totals for each conference in every year listed below
for conference in conferences:
    # Get list of teams
    teams = get_teams(conference)

    # List of years
    years = ['2023']

    for year in years:
        win_count = 0
        lose_count = 0
        game_count = 0

        for team in teams:

            # Get the data from the Firestore database
            school = f'{team}'
            collect = f'{year}GameLog'
            data_ref = db.collection(conference).document(school).collection(collect)
            data_docs = data_ref.stream()

            # Count each win and loss
            for doc in data_docs:
                data = doc.to_dict()
                if data['Result'] == "W":
                    win_count += 1
                    game_count += 1
                elif data['Result'] == "L":
                    lose_count += 1
                    game_count += 1
                else:
                    print(f'no win or loss for {data["Date"]}')

        # Verify that all totals are equal
        print(f'{conference} {year}:\n{win_count} wins\n{lose_count} losses\n{game_count} games\n')
