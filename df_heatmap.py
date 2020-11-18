import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

pd.options.mode.chained_assignment = None 


#import our CSV file 
df = pd.read_csv('2019.csv')

#drop uneccessary colums
df.drop(['Rk', '2PM', '2PP', 'FantPt', 'DKPt', 'FDPt', 'VBD', 'PosRank', 'OvRank', 
        'PPR', 'Fmb', 'GS', 'Age', 'Tgt', 'Y/A', 'Att', 'Att.1', 'Cmp', 'Y/R'], axis=1, inplace=True)

#fix name formatting
df['Player'] = df['Player'].apply(lambda x: x.split('*')[0]).apply(lambda x: x.split('\\')[0])

#rename columns
df.rename({
    'TD': 'PassingTD',
    'TD.1': 'RushingTD',
    'TD.2': 'ReceivingTD',
    'TD.3': 'TotalTD',
    'Yds': 'PassingYDs',
    'Yds.1': 'RushingYDs',
    'Yds.2': 'ReceivingYDs',
}, axis=1, inplace=True)

"""Extra Stuff before we partition DataFrames by position."""

#Make sure to put paranthesis if you break lines.
df['FantasyPoints'] = (df['PassingYDs']*0.04 + df['PassingTD']*4 - df['Int']*2 + df['RushingYDs']*0.1 + df['RushingTD']*6 + df['Rec']*1 + df['ReceivingYDs']*0.1 + df['ReceivingTD']*6 - df['FL']*2)

df['FantasyPoints/GM'] = df['FantasyPoints']/df['G']

#Setting up heatmap chart
#df = df[['Tm', 'FantPos', 'FantasyPoints', 'FantasyPoints/GM']]

#Unfortnately, our DataFrame is limited.
df = df[df['Tm'] != '2TM']
df = df[df['Tm'] != '3TM']

"""End Extra Stuff"""

#seperate dataframes based off position
rb_df = df[df['FantPos'] == 'RB']
qb_df = df[df['FantPos'] == 'QB']
wr_df = df[df['FantPos'] == 'WR']
te_df = df[df['FantPos'] == "TE"]

# RB Receptions over 5 per game
rb_df['Rec/G'] = rb_df['Rec']/rb_df['G']
rb_df = rb_df[rb_df['Rec'] > 5]

#Setting up heatmap chart
qb_df = qb_df[['Tm', 'FantPos', 'FantasyPoints', 'FantasyPoints/GM']]
rb_df = rb_df[['Tm', 'FantPos', 'FantasyPoints', 'FantasyPoints/GM']]
wr_df = wr_df[['Tm', 'FantPos', 'FantasyPoints', 'FantasyPoints/GM']]
te_df = te_df[['Tm', 'FantPos', 'FantasyPoints', 'FantasyPoints/GM']]


# Sort players by position rank on respected team

def get_top_players(df, n):
    return df.groupby('Tm').apply(lambda x: x.nlargest(n, ['FantasyPoints']).min()).reset_index(drop=True)

qb_df = get_top_players(qb_df, 1)
te_df = get_top_players(te_df, 1)
rb1_df = get_top_players(rb_df, 1)
rb2_df = get_top_players(rb_df, 2)
wr1_df = get_top_players(wr_df, 1)
wr2_df = get_top_players(wr_df, 2)
wr3_df = get_top_players(wr_df, 3)
 
new_names = {
    'QB1': qb_df,
    'TE1': te_df,
    'RB1': rb1_df,
    'RB2': rb2_df,
    'WR1': wr1_df,
    'WR2': wr2_df,
    'WR3': wr3_df
}

# print(rb2_df)


for name, new_df in new_names.items():
    new_df.rename({'FantasyPoints/GM': name}, axis=1, inplace=True)
    new_df.drop(['FantPos', 'FantasyPoints'], axis=1, inplace=True)
    new_df.set_index('Tm', inplace=True)

df = pd.concat([qb_df, te_df, rb1_df, rb2_df, wr1_df, wr2_df, wr3_df], axis=1)

corrMatrix = df.corr()

fig, ax = plt.subplots()
fig.set_size_inches(15, 10)

cmap = sns.diverging_palette(0, 250, as_cmap=True)

mask = np.zeros_like(corrMatrix, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

vizCorrMatrix = sns.heatmap(corrMatrix, mask=mask, cmap=cmap, center=0)

plt.show()
