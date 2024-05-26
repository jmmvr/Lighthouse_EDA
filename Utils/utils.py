import pandas as pd
import numpy as np
import seaborn as sns

def import_quick_data(file_in: str) -> pd.core.frame.DataFrame:
    """
    Function to quickly import and access the info in the source
    """
    
    print('###############################################')
    print(f'####### {file_in} #######')
    print('###############################################')
    
    df = pd.read_csv(file_in)
    print(f"shape is: {df.shape}")
    print(f"# of rows we missing values in some field: {sum([True for idx,row in df.iterrows() if any(row.isnull())])}")    
    print('Dtypes', df.dtypes, sep ='\n')
    print('Describe fields:', df.describe(), sep = '\n')
    
    numerics = ['float16', 'float32', 'float64']
    sns.boxplot(
        x="variable", 
        y="value", 
        data=pd.melt(df.select_dtypes(include=numerics))
        )
        
    df.select_dtypes(include=numerics).hist(bins=12)
    plt.show()
    
    print('###############################################')
    print(f'####### Ending call... #######')
    print('###############################################')
    print('')
    
    return df

# from scipy import stats for testing equality of variances and means in review_score, stars, and room_count
def equality_of_groups_2class(df: pd.core.frame.DataFrame, group_var: str , vars_test: list):
    
    """
    
    Function to access equality of variances and means across a 2 class group
    
    """
    
    tstats = {}
    a_filter = df[group_var] == df[group_var].unique()[0]
    group1_str = df[group_var].unique()[0]
    group2_str = df[group_var].unique()[1]
    
    for x in vars_test:

        print(x)
        print(f"Equality of variances across {group_var}, using leven test")
        t, p = levene(
            df[x][a_filter].dropna(), 
            df[x][~a_filter].dropna(),
            center='mean'
        )
        if p < 0.05:
            print(f"P-value is {round(p, 3)} -> Field {x}'s variance is statistically different between {group1_str} and {group2_str}")
        else:
            print(f"P-value is {round(p, 3)} -> Field {x}'s variance is not statistically different between {group1_str} and {group2_str}")    

        print(f"Equality of means in across groups in {group_var}, using t test")
        t, p = stats.ttest_ind(
            df[x][a_filter].dropna(), 
            df[x][~a_filter].dropna()
        )

        if p < 0.05:
            print(f"P-value is {round(p, 3)} -> Field {x}'s mean is statistically different between {group1_str} and {group2_str}")
        else:
            print(f"P-value is {round(p, 3)} -> Field {x}'s mean is not statistically different between {group1_str} and {group2_str}")

        print('')

    print(f"Group by {group_var}:",df.groupby(group_var)[test_vars].mean().reset_index(), sep = '\n')

    return