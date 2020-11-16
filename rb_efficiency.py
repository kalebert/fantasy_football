from rb_usage import *

# How does efficiency correlate to fantasy football performace? 
rb_df['TD/Usage'] = (rb_df['RushingTD']+ rb_df['ReceivingTD'])/(rb_df['RushingAtt'] + rb_df['Tgt'])

# Make sure there is an adequete sample size

fig, ax = plt.subplots()
fig.set_size_inches(15, 10)

rb_df = rb_df[rb_df['RushingAtt'] > 20 ]

plot = sns.regplot(
    x = rb_df['TD/Usage'],
    y = rb_df['FantasyPoints/GM'],
    scatter=True)

plt.show()