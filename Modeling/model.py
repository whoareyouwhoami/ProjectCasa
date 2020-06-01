import re
import os
import sys
import numpy as np
import pandas as pd
import warnings

from statsmodels.tsa.vector_ar.var_model import VAR

warnings.filterwarnings("ignore")

class PredictModel:
    def __init__(self, apartment_name, apartment_area):
        self.src_root = os.path.dirname(os.path.realpath(__file__))

        # User input
        self.apartment_name = apartment_name
        self.apartment_area = int(apartment_area)


    def _model_data(self):
        # DataFrame
        try:
            price_df = pd.read_pickle(os.path.join(self.src_root, 'data', 'apartment_price.pkl'))
            clustered_df = pd.read_pickle(os.path.join(self.src_root, 'data', 'clustered_apartment.pkl'))
        except:
            raise ValueError('Check if files exist!')

        dataframe = price_df.merge(clustered_df, how='left', on='apartment_id')

        dataframe['area'] = dataframe['area'].apply(lambda x: int(re.split('\D', x)[0]))
        dataframe['period'] = pd.to_datetime(dataframe['period'], format='%Y.%m')

        self.group_name = clustered_df.loc[clustered_df['apartment_name'] == self.apartment_name, 'cluster'].values[0]

        return dataframe

    def _model_clean(self):
        dataframe = self._model_data()

        temp = dataframe[(dataframe['cluster'] == self.group_name) &
                  (dataframe['area'] <= self.apartment_area + 3) &
                  (dataframe['area'] >= self.apartment_area - 3)]
        try:
            date_range = pd.date_range(start=temp.loc[temp['apartment_name'] == self.apartment_name, 'period'].min(),
                                       end=temp['period'].max(),
                                       freq='MS')
        except ValueError:
            return False

        exist = (temp.loc[temp['apartment_name'] == self.apartment_name].groupby('period')['amount'].agg([self.Q1, self.Q2, self.Q3], ).reset_index())

        empty_date = date_range[~date_range.isin(exist['period'])]

        supply = (temp.groupby('period')['amount'].agg([self.Q1, self.Q2, self.Q3]).reset_index())

        total = (pd.concat([exist, supply.loc[supply['period'].isin(empty_date)]], axis=0).sort_values('period').set_index(keys='period') / 10000000)

        return total

    def extract_model(self, input):
        total = self._model_clean()

        if total is False:
            return "Try to find available area by:\n  sh casa.sh --find aptartment name\n"

        # input
        n = int(input)

        new_index = pd.date_range(start=total.index[-1], periods=n + 1, freq='MS')[1:]

        model = VAR(total)
        model_fit = model.fit()
        pred = model_fit.forecast(y=total.values, steps=n)

        pred = pd.DataFrame(pred, columns=['Q1', 'Q2', 'Q3'], index=new_index)
        final_df = pd.concat([total, pred], axis=0)

        final = final_df.loc[new_index]

        return final

    def Q1(self, x):
        return np.percentile(x, 0.25)

    def Q2(self, x):
        return np.percentile(x, 0.5)

    def Q3(self, x):
        return np.percentile(x, 0.75)


# apartment_name = '당산반도유보라팰리스'
# apartment_area = 108
# months = 5

apartment_name = sys.argv[1]
apartment_area = sys.argv[2]
months = sys.argv[3]

predict_model = PredictModel(apartment_name, apartment_area)
result = predict_model.extract_model(input=months)

exit(result)