import pandas as pd
import datetime as dt
from typing import Tuple


class EmlParser:

    @staticmethod
    def parse(html: str, invoice_number: int) -> Tuple[dict, dt.datetime, dt.datetime]:

        html_df = pd.read_html(html, keep_default_na=False)[0]
        idx = html_df.index[html_df[0] == 'Invoice']  # get invoices count and start index

        currency = html_df[5][html_df[5] != 'total'].str.split(' ').str[0]
        html_df[6] = currency  # create Currency column

        # stay only numbers in number cols
        numeric_cols = html_df.columns[3:-1].to_list()
        html_df[numeric_cols] = html_df[numeric_cols].replace(
            '[€ ,]', '', regex=True).replace('[-,]', '0', regex=True)

        columns = ['Item', 'QTY', 'Rate', 'Total', 'Currency']
        invoices = {}

        for i in range(len(idx)):

            if (i + 1) < len(idx):  # if not last iteration
                df = html_df.loc[idx[i] + 2: idx[i + 1] - 3]

            if (i + 1) == len(idx):  # if last iteration
                start = idx[i] + 1
                stop = html_df.index.max() - idx.size - i
                df = html_df.loc[start: stop]

            if df is not None:
                df[numeric_cols] = df[numeric_cols].astype(float)   # to floats

                # concat tree first cols
                cols = [0, 1, 2]
                df.insert(loc=0, column='Item', value=html_df[cols].agg(' '.join, axis=1))

                # drop concatenated cols
                df.drop(cols, axis=1, inplace=True)
                df.columns = columns

                invoices[invoice_number] = df
                invoice_number += 1

        return invoices
