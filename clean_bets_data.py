import pandas as pd
import re
from nanoid import generate

# Path to CSV file
csv_file = '~/ab_active_bets.csv'

# Functions
def clean_bet_side(bet_side):
    return re.sub(r'[\d+\-\.\,]', '', bet_side).strip()

def generate_bet_id():
    return generate('0123456789abcdef', 8) + "-" + generate('0123456789abcdef', 4) + "-" + generate('0123456789abcdef', 4)+ "-" + generate('0123456789abcdef', 4)+ "-" + generate('0123456789abcdef', 12)

def calculate_profit(row):
    if row['bet_status'] =='WON':
        return (row['wager'] * row['price']) - row['wager']
    elif row['bet_status'] == 'LOST':
        return -row['wager']
    else:
        return 0

# Load the CSV file
df = pd.read_csv(csv_file)


# Clean the data
df['bet_selection'] = df['betSide'].apply(clean_bet_side)
df['point'] = df['spread'].combine_first(df['gameTotal'])
df['point'] = df['point'].fillna('')
df['betType'] = df['betType'].replace({
    'MONEYLINE':'Moneyline',
    'TOTALS':'Totals',
    'SPREAD':'Spreads'
})

df['betId'] = df.apply(lambda _:generate_bet_id(),axis=1)

# Drop unneeded columns and rename to match db
df.drop(columns=['spread','gameTotal','betSide'], inplace=True)
df.rename(columns={
    'betId':'bet_id',
    'userId':'user_id',
    'sportKey':'sport_key',
    'time':'event_date',
    'league':'sport',
    'gameId':'game_id',
     'betType':'market',
     'homeTeam':'home_team',
     'awayTeam':'away_team',
     'odds':'price',
     'betStatus':'bet_status'
}, inplace=True)

# Calculate profit and add it as a new column
df['profit'] = df.apply(calculate_profit, axis=1)


final_df = df[['bet_id','user_id','sport_key','sportsbook','event_date','sport','game_id','home_team','away_team','market','bet_selection','price','point','wager','bet_status','profit' ,'email']]


final_df.to_csv('cleaned_file.csv',index=False)
print("Data cleaned, organized, and saved to 'cleaned_file.csv'")
