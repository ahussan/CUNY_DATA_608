import pandas as pd
import numpy as np
import string as s
'''
borocode: 1 (Manhattan), 2 (Bronx), 3 (Brooklyn), 4 (Queens), 5 (Staten Island)
'''
def get_all_tree_data():
    max_limit = 1000
    #df_size = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$select=count(tree_id)')

    url_with_limit_no_offset = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit='+ str(max_limit) +
                '&$select=borocode,spc_common,health,steward,count(tree_id)' +
                '&$group=borocode,spc_common,health,steward').replace(' ', '%20')


    url_with_limit_offset = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit='+ str(max_limit) +\
                '&$select=borocode,spc_common,health,steward,count(tree_id)' +\
                '&$group=borocode,spc_common,health,steward' + '&$offset='


    all_trees_with_zero_offset = pd.read_json(url_with_limit_no_offset)
    all_trees_in_the_borough = pd.DataFrame(columns=list(all_trees_with_zero_offset.columns.values))
    all_trees_in_the_borough = all_trees_in_the_borough.append(all_trees_with_zero_offset)

    print('shape after first call '+ str(len(all_trees_in_the_borough)))

    for x in range(1, 5):
        print(url_with_limit_offset + str(max_limit * x))
        new_data_set = pd.read_json(url_with_limit_offset + str(x))
        all_trees_in_the_borough = all_trees_in_the_borough.append(new_data_set)
        print('shape after '+str(x) +' call : '+str(len(all_trees_in_the_borough)))
    all_trees_in_the_borough.reset_index(drop=True)

    all_trees_in_the_borough = all_trees_in_the_borough.dropna()
    all_trees_in_the_borough = all_trees_in_the_borough.replace('None','0_stewards')
    return all_trees_in_the_borough
