import re
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

from statsmodels.tsa.vector_ar.var_model import VAR

warnings.filterwarnings("ignore")

class PredictModel:
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

    def _model_eval(self, df, input):
        input = int(input)

        train = df[:-input]
        test = df[-input:]

        model = VAR(train)
        model_fit = model.fit()

        yhat = model_fit.forecast(y=train.values, steps=4)
        var = pd.DataFrame(yhat,
                           columns=['Q1_hat', 'Q2_hat', 'Q3_hat'],
                           index=test.index)

        result = pd.concat([test, var], axis=1)

        return result

    def extract_model(self, input, save_status=False):
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

        if save_status is True:
            self._save_image_model(eval_model=final_df, pred_model=pred, pred_num=input)

        return final

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
save_status = sys.argv[4]

if save_status == 'false':
    status = False
else:
    status = True

predict_model = PredictModel(apartment_name, apartment_area)
result = predict_model.extract_model(input=months, save_status=status)

exit(result)
#
# print(result.loc[new_index])
# result[-(n+6):].plot(kind='line') # 결과물은 이전과 비교하기 위해 6개월 전부터 시각화
# plt.title(f"{user_option['apartment_name']}_{result.index[0].strftime('%Y%m%d')}_{result.index[-1].strftime('%Y%m%d')}")
# plt.vlines(x=pred.index[0], ymin=0, ymax=result.max(), color='red')
# plt.ylabel('천 만 원')
# plt.savefig(f"./output/{user_option['apartment_name']}_{result.index[0].strftime('%Y%m%d')}_{result.index[-1].strftime('%Y%m%d')}.png",
#            dpi=300)
# plt.show()