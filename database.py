import pandas as pd
from pandas import to_datetime
from pandas import DataFrame


class ReadFile:
    def __init__(self, path_file):
        self._path_file = path_file
        self._content_data = pd.read_excel(self._path_file, header=0)

    @property
    def get_frame_size(self) -> int:
        return self._content_data.shape[0]

    @property
    def get_raw_data(self) -> pd.DataFrame:
        return self._content_data


class PrepareData:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def prepare(self) -> pd.DataFrame:
        try:
            prepared_df = self.data
            prepared_df.columns = ['ds', 'y']
            prepared_df['ds'] = to_datetime(prepared_df['ds'])
            prepared_df['y'] = prepared_df['y'].astype(float)
            return prepared_df
        except ValueError as e:
            return e


class Data(ReadFile):
    def __init__(self, file, tail: int = 0):
        self.tail = tail
        super().__init__(file)

    @property
    def get_data_tail(self) -> pd.DataFrame:
        return PrepareData(self.get_raw_data.loc[self.get_frame_size - self.tail:]).prepare()

    @property
    def get_data_no_tail(self) -> pd.DataFrame:
        return PrepareData(self.get_raw_data.loc[:self.get_frame_size - self.tail - 1]).prepare()

    @property
    def get_last_date(self) -> pd.DataFrame:
        return self.get_raw_data.iloc[self.get_frame_size - 1 - self.tail][0]


class MakeFrame:
    @staticmethod
    def result(data: list[[str]]) -> pd.DataFrame:
        df = DataFrame(data)
        df.columns = ['ds']
        df['ds'] = to_datetime(df['ds'])
        return df
