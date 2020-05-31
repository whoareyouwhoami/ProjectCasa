import os
import re
import sys
import numpy as np
import pandas as pd

pd.set_option("display.max_columns", 2000)
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 1000)

name = sys.argv[1]

src_dir = os.path.dirname(os.path.realpath(__file__))
file_dir = os.path.join(src_dir, 'data/casa_list.pkl')

casa_df = pd.read_pickle(file_dir)

casa_filter = casa_df.loc[casa_df['apartment_name'] == name]['area']

if casa_filter.empty:
    print('Nothing is listed for', name)
else:
    available_area = np.unique(casa_filter)

    print('Available area for ' + name + ':')
    for area in available_area:
        final = re.search('[0-9]+', area).group()
        print(final)


