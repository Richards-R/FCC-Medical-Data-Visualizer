import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1
#print(df['cholesterol'].value_counts())

df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1
#print(df['gluc'].value_counts())

# Add 'overweight' column
df['overweight'] = (df['weight']/((df['height']*0.01)**2)) 
df.loc[df['overweight'] <= 25, 'overweight'] = 0 
df.loc[df['overweight'] > 25, 'overweight'] = 1
df['overweight'] = (df['overweight']).astype(int)
#print(df['overweight'].value_counts())

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.


# Draw Categorical Plot
def draw_cat_plot():
    
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = df.melt(id_vars= 'cardio', value_vars=['active', 'alco', 'cholesterol', 'gluc',   'overweight', 'smoke'])
    #print('melted_df\n', df_cat.sample(50))

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.

    # Draw the catplot with 'sns.catplot()'
    # Get the figure for the output
    fig = sns.catplot(data=df_cat, kind ="count", hue="value", x= 'variable', col = 'cardio')
    fig.set_axis_labels("variable", "total")
    fig = fig.fig
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & 
            (df['height'] >= df['height'].quantile(0.025)) &
            (df['height'] <= df['height'].quantile(0.975)) &
            (df['weight'] >= df['weight'].quantile(0.025)) & 
            (df['weight'] <= df['weight'].quantile(0.975))]
    
    # Calculate the correlation matrix
    corr = df_heat.corr()
    #print('corr\n', corr.shape)

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    #print('mask\n', mask.shape)
   
    # Set up the matplotlib figure
    fig = plt.figure(frameon=False)
    
    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, annot=True, fmt='0.1f')
    
    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig