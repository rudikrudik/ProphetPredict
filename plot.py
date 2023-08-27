import matplotlib.pyplot as plt
from standard import STANDARD_THEMES as themes


class Plot:
    """ Создание графика
    :argument
    actual -- pd.DataFrame исторические данные
    predict -- pd.DataFrame предсказание данных за период
    merge_graph -- связывание графиков для непрерывной линии
    """
    def __init__(self, actual, predict, merge_graph: bool = False):
        self.merge = merge_graph
        self._actual_dates = actual['ds'].values
        self._actual_data = actual['y'].values
        self._predicted_dates = predict['ds'].values
        self._predicted_data = predict['yhat'].values
        self.start = [self._actual_dates[-1], self._predicted_dates[0]]
        self.end = [self._actual_data[-1], self._predicted_data[0]]

    def draw(self, style_theme):
        fig, ax = plt.subplots(1)
        fig.patch.set_facecolor(themes[style_theme]['colors']['bg'])
        ax.set_facecolor(themes[style_theme]['colors']['active'])

        for axes in ['x', 'y']:
            ax.tick_params(axis=axes, colors=themes[style_theme]['colors']['fg'])

        for side in ['left', 'right', 'top', 'bottom']:
            ax.spines[side].set_color(themes[style_theme]['colors']['secondary'])

        ax.plot(self._actual_dates, self._actual_data, label='Actual',
                color=themes[style_theme]['colors']['primary'], alpha=0.9)
        ax.plot(self._predicted_dates, self._predicted_data, label='Predicted',
                color=themes[style_theme]['colors']['danger'], alpha=0.9)

        if self.merge:
            ax.plot(self.start, self.end, color='red')
        ax.legend()
        ax.grid(color=themes[style_theme]['colors']['inputbg'])
        fig.autofmt_xdate()
        return fig
