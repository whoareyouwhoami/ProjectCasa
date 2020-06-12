import re
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

from statsmodels.tsa.arima_model import ARIMA

warnings.filterwarnings("ignore")

pd.set_option("display.max_columns", 2000)
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 1000)

class CleanModel:
    def __init__(self, apartment_name, apartment_area):
        self.src_root = os.path.dirname(os.path.realpath(__file__))
        self.root = os.path.realpath(os.curdir)

        # User input
        self.apartment_name = apartment_name
        self.apartment_area = int(apartment_area)

    def _model_data(self):
        # DataFrame
        try:
            price_df = pd.read_pickle(os.path.join(self.src_root, 'data', 'apartment_price.pkl'))
            clustered_df = pd.read_pickle(os.path.join(self.src_root, 'data', 'apartment_cluster.pkl'))
            apartment_df = pd.read_pickle(os.path.join(self.src_root, 'data', 'apartment_table.pkl'))
        except:
            raise ValueError('Check if files exist!')

        price_df['area'] = price_df['area'].apply(lambda x: int(re.split('\D', x)[0]))
        apartment_df = apartment_df[['apartment_id', 'apartment_name']]

        dataframe = apartment_df.merge(clustered_df, how='left', on='apartment_id').merge(price_df, how='left', on='apartment_id')
        dataframe['period'] = pd.to_datetime(dataframe['period'], format='%Y.%m')
        dataframe = dataframe[['period', 'apartment_name', 'area', 'amount', 'cluster']]

        group_name = dataframe.loc[dataframe['apartment_name'] == self.apartment_name, 'cluster'].values[0]

        return dataframe, group_name

    def _model_clean(self):
        dataframe, group_name = self._model_data()

        chosen_cluster = dataframe[dataframe['cluster'] == group_name]

        empty_df = dataframe['period'].sort_values().reset_index()
        empty_df = empty_df.dropna(axis=0).drop_duplicates(['period'])

        temp = dataframe[(dataframe['apartment_name'] == self.apartment_name) &
                  (dataframe['area'] <= self.apartment_area + 3) &
                  (dataframe['area'] >= self.apartment_area - 3)]

        t = empty_df.merge(temp, how='left', on='period')

        t.groupby(t['period']).mean()
        t = t.reset_index()
        t = t[['period', 'amount']]

        starting_point = t[t['amount'].notnull()].index[0]
        ending_point = t[t['amount'].notnull()].index[-1]

        t = t[starting_point:ending_point + 1].reset_index()
        t = t[['period', 'amount']]

        stopping = True
        for index, row in t.iterrows():
            if np.isnan(t['amount'][index]):
                new_index = index
                starts = t['amount'][index - 1]

                while stopping:
                    if np.isnan(t['amount'][new_index + 1]):
                        new_index += 1
                    else:
                        ends = t['amount'][new_index + 1]
                        stopping = False

                new = chosen_cluster[chosen_cluster['period'] == t['period'][index]]

                if starts > ends:
                    groups = new[(new['amount'] <= starts) & (new['amount'] >= ends)]
                else:
                    groups = new[(new['amount'] <= ends) & (new['amount'] >= starts)]

                if groups.empty:
                    t['amount'][index] = (starts + ends) / 2
                else:
                    t['amount'][index] = groups['amount'].max()

        t = t.set_index('period')

        return t


class PredictModel(CleanModel):
    def __init__(self, apartment_name, apartment_area):
        super().__init__(apartment_name, apartment_area)

    def _save_image_model(self, eval_model, pred_model, pred_num):
        pred_num = int(pred_num)

        fig = eval_model[-(pred_num + 6):].plot(kind='line')

        plt.title("Prediction")
        plt.vlines(x=pred_model.index[0], ymin=0, ymax=eval_model.max(), color='red')
        plt.ylabel('₩ 100,000,000')

        # Prediction Image Output
        pred_output_dir = os.path.join(self.root, 'pred_output')

        if not os.path.exists(pred_output_dir):
            os.mkdir(pred_output_dir)

        save_name = self.apartment_name + f"_{eval_model.index[0].strftime('%Y%m%d')}_{eval_model.index[-1].strftime('%Y%m%d')}.png"
        save_path = os.path.join(pred_output_dir, save_name)

        plt.savefig(save_path, dpi=300)


    def extract_model(self, input):
        total = self._model_clean()

        if total is False:
            return "Try to find available area by:\n  sh casa.sh --find aptartment name\n"

        n = int(input)

        model = ARIMA(total, order=(0, 1, 1))
        model_fit = model.fit(trend='c', full_output=True, disp=False)
        predict = model_fit.forecast(steps=n)

        arima = pd.DataFrame(predict[0])
        arima.columns = ['arima']
        arima.index = total[-n:].index

        final_df = pd.concat([total[-n:], arima], axis=1)
        final_df.columns = ['real', 'model']
        final_df['model'] = final_df['model'].map(int)
        final_df['model'] = final_df['model'].apply(lambda x: "{:,}".format(x))
        final = final_df['model'].reset_index()

        final = final.rename(columns={"period":"Period", "model":"Price"})

        period_list = []
        for i in range(len(final['Period'])):
            if i == 0:
                append_name = "+" + str(i + 1) + " month "
            else:
                append_name = "+" + str(i + 1) + " months"

            period_list.append(append_name)

        period_temp = pd.DataFrame({"Period":period_list})

        output = pd.merge(period_temp, final['Price'],  left_index=True, right_index=True)

        return output.to_string(index=False)


# apartment_name = '당산반도유보라팰리스'
# apartment_area = 108
# months = 5

apartment_name = sys.argv[1]
apartment_area = sys.argv[2]
months = sys.argv[3]

predict_model = PredictModel(apartment_name, apartment_area)
result = predict_model.extract_model(input=months)

exit(result)