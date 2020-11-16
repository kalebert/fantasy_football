from fantasy_df_setup import *

# How did Targets + Rushing TDs correlate to fantasy points per game for RBs in 2019? 

# Create new column to calculate fantasy points scored (Note: this is full PPR)
rb_df['FantasyPoints'] = rb_df['RushingYDs']*0.1 + rb_df['RushingTD']*6 + rb_df['Rec'] + rb_df['ReceivingYDs']*0.1 + rb_df ['ReceivingTD']*6 - rb_df['FL']*2

# Create new column for Fantasy points per game
rb_df['FantasyPoints/GM'] = rb_df['FantasyPoints']/rb_df['G']
rb_df['FantasyPoints/GM'] = rb_df['FantasyPoints'].apply(lambda x: round(x, 2))

#Creat new column for usage per game. Usage is defined as # of targets + carries
rb_df['Usage/GM'] = (rb_df['RushingAtt'] + rb_df['Tgt'])/rb_df['G']
#Round each row value to two decimal places
rb_df['Usage/GM'] = rb_df['Usage/GM'].apply(lambda x: round(x, 2))

# Create a new column for rushing attempts per game
rb_df['RushingAtt/GM'] = rb_df['RushingAtt']/rb_df['G']
#round each row value to two decimal places
rb_df['RushingAtt/GM'] = rb_df['RushingAtt/GM'].apply(lambda x: round(x , 2))

#just for styling, we imported seaborn earlier as sns. 
sns.set_style('whitegrid')

#create a canvas with matplotlib
fig, ax = plt.subplots()
fig.set_size_inches(15, 10)

#basic regression scatter ploy with trendline
plot = sns.regplot(
    x=rb_df['Usage/GM'],
    y=rb_df['FantasyPoints/GM'],
    scatter=True,
)

# plt.show()