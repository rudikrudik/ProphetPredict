class TestPredict:
    """ Тестирование результата предсказания.
    :argument
    test -- pd.DataFrame выборка исторических данных.
    predict -- pd.DataFrame результат предсказания
    :return
    Список - (дата, результат) отклонения предсказания от исторических данных в процентах
    """
    def __init__(self, test, predict):
        self._test_list = test['y'].to_list()
        self._predict_list = predict['yhat'].to_list()
        self._date_list = test['ds'].to_list()
        self.error_list = []

        for date, test, predict in zip(self._date_list, self._test_list, self._predict_list):
            self.error_list.append((str(date).split(' ')[0], (abs(predict - test) / test) * 100))

    @property
    def get_result(self) -> list[tuple[str, float]]:
        return self.error_list
