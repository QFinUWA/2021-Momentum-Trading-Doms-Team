# -*- coding: utf-8 -*-
"""
    csv_tools
    ~~~~~~~~~
    merge CSV files

    Log:
        20210819

"""

__version__ = '0.1'

import os
import math

import pandas as pd


class Res:
    """
        merge
    """

    def __init__(self):
        self.df = None

    @classmethod
    def file_adapter(cls, file_path):
        """
        :param file_path:
        :return:
        """
        file_name = os.path.basename(file_path)
        if file_name.find('USDT_') == -1:
            return None
        df = pd.read_csv(file_path)
        df.columns = ['date'] + [f"{file_name.replace('USDT_', '').replace('.csv', '')}_{_}" for _ in df.columns[1:]]
        return df

    def append_file(self, file_path):
        """
            merge file
        :param file_path:
        :return:
        """
        df = self.file_adapter(file_path)
        if df is not None:
            if self.df is None:
                self.df = df
            else:
                self.df = pd.merge(self.df, df, on='date', how='inner')

    def export_to_csv(self, file_name='price.csv'):
        """
            Export results
        :param file_name:
        :return:
        """
        self.df.to_csv(file_name)

    def make_up(self, base_path='./data/'):
        """
            Merge files under folder
        :param base_path:
        :return:
        """
        for csv_file_path in [f"{base_path}{_}" for _ in os.listdir(base_path)]:
            self.append_file(csv_file_path)

    def math_calculate(self, math_ways: dict, export_file_name='return.csv'):
        """
            calculate return
        :param math_ways:
        :param export_file_name:
        :return:
        """

        last_row = self.df.iloc[0]
        result_dict = {}
        for col in self.df.columns:
            if col.find('_') != -1:
                k, v = col.split('_')
                for math_way in math_ways.keys():
                    result_dict[f"{k}_{math_way}_{v}"] = {
                        'way': math_way,
                        'col': col,
                        'values': ['',]
                    }

        for ind, row in self.df[1:].iterrows():
            for k, v in result_dict.items():
                try:
                    v['values'].append(math_ways[v['way']](last_row[v['col']], row[v['col']]))
                except Exception as e:
                    v['values'].append('')
            last_row = row

        res_d = {
            'date': self.df.date.to_list()
        }
        for k, v in result_dict.items():
            res_d[k] = v['values']

        pd.DataFrame(res_d).to_csv(export_file_name)


if __name__ == '__main__':
    base_path = 'C:\\Users\\jessi\\Dropbox\\Trading_Project\\DJT-Crypto-Bot\\'
    res = Res()
    res.make_up(base_path + 'data\\')
    res.export_to_csv(base_path + 'mergedata\\price.csv')
    res.math_calculate({
        'R': lambda x, y: (y - x) / x,
        'log': lambda x, y: math.log(y / x)},
        base_path + 'mergedata\\return.csv'
    )

