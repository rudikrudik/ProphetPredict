from dateutil.relativedelta import *
from prophet import Prophet


class ProphetDataPredict:
    """ Обучение на модели
    :argument
    model_learning -- pd.DataFrame данные для обучения.
    month_predict_frame -- pd.DataFrame с заданным количеством месяцев для результата.
    :return
    pd.DataFrame с результатом предсказания
    """
    def __init__(self, model_learning, month_predict_frame):
        self.predict_frame = month_predict_frame
        self.model = Prophet()
        self.model.fit(model_learning)
        self.predict = self.model.predict(self.predict_frame)[['ds', 'yhat']]


class PredictMonth:
    """ Формирование списка дат по месяцам.
    :argument
    start_data -- datetime с какого числа начинать список
    month -- количество месяцев
    :return
    список datetime
    """
    @staticmethod
    def month(start_data, month: int):
        month_timestamp_list = []
        for m in range(1, month + 1):
            month_timestamp_list.append([start_data + relativedelta(months=+m)])
        return month_timestamp_list
