import database
import tkinter
import tkinter as ttk

from database import Data, MakeFrame
from prophet_predict import ProphetDataPredict, PredictMonth
from test_predict_result import TestPredict
from plot import Plot
from tkinter import ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prophet Predict")
        self.geometry("1000x600")
        self.style = Style('flatly')
        self.path_var = tkinter.StringVar()
        self.read_file_data = tkinter.StringVar()
        self.file_info = tkinter.StringVar(value='0')
        self.predict_data_label = tkinter.StringVar()
        self.slider_data_month = tkinter.StringVar()
        self.slider_month_predict = tkinter.StringVar()
        self.month_slider = ttk.Scale()
        self.notebook = ttk.Notebook()
        self.test_tab = ttk.Frame()
        self.predict_tab = ttk.Frame()
        self.plot_canvas = FigureCanvasTkAgg()
        self.result_frame = ttk.LabelFrame()
        self.create_path_row()
        self.create_settings()
        self.result()

    # Функции создания виджетов
    def create_path_row(self):
        # Фрейм с путем до файла и кнопки открыть
        file_frame = ttk.LabelFrame(master=self, text='Select the path to the file:')
        file_frame.pack(fill=X, padx=(20, 20), pady=(20, 20))

        path_label = ttk.Label(master=file_frame, text='File Path:')
        path_label.pack(side=LEFT, padx=(20, 0), pady=(10, 15))

        file_path = ttk.Entry(master=file_frame, textvariable=self.path_var)
        file_path.pack(side=LEFT, fill=X, expand=True, padx=(20, 20), pady=(10, 15))

        btn_open = ttk.Button(master=file_frame, text='Open File', command=self.open_file)
        btn_open.pack(side=RIGHT, padx=(0, 20), pady=(10, 15))

    def create_settings(self):
        self.notebook = ttk.Notebook(self, bootstyle="secondary", width=200)
        self.notebook.pack(side=LEFT, fill=Y, padx=(20, 20), pady=(0, 20))
        # Вкладка Settings
        settings_tab = ttk.Frame(self.notebook, padding=10)
        # Кнопка чтения данных из файла
        read_file_btn = ttk.Button(settings_tab, text='Read File', command=self.read_file)
        read_file_btn.pack()
        # Фрейм для информации о файле
        file_info = ttk.LabelFrame(settings_tab, text='File Info:')
        file_info.pack(fill=X, anchor=S, pady=(20, 20))
        file_about = ttk.Label(file_info, text='Frame Size:')
        file_about.pack(side=LEFT, padx=(10, 0), pady=(0, 10))
        file_about_frame_size = ttk.Label(file_info, text='', textvariable=self.file_info)
        file_about_frame_size.pack(side=LEFT, pady=(0, 10))
        # Фрейм об авторе
        author_frame = ttk.LabelFrame(settings_tab, text='Author:')
        author_frame.pack(fill=X, anchor=S, pady=(0, 20))
        author_name = ttk.Label(author_frame, text='Name: Rudolf Bachman')
        author_name.pack(side=LEFT, padx=(10, 0), pady=(5, 10))

        # Фрейм для выбора темы
        theme_frame = ttk.LabelFrame(settings_tab, text='Choose Theme:')
        theme_frame.pack(fill=X, anchor=S)

        # Кнопка смены темы
        list_themes = ['Default', 'Flatly', 'Litera', 'Pulse', 'Cosmo', 'Superhero', 'Darkly', 'Vapor']
        name_theme = tkinter.StringVar()
        choose_theme = ttk.OptionMenu(theme_frame, name_theme, *list_themes, command=self.change_theme)
        choose_theme.pack(fill=X, padx=(10, 10), pady=(10, 10))

        # Вкладка Test
        self.test_tab = ttk.Frame(self.notebook, padding=10)
        # Фрейм выбора количества месяцев
        cut_month = ttk.LabelFrame(self.test_tab, text='Cut tail month:')
        cut_month.pack(fill=X)

        self.month_slider = ttk.Scale(master=cut_month, orient=HORIZONTAL, command=self.slider_data)
        self.month_slider.pack(fill=X, padx=(10, 10), pady=(10, 10))

        month_slider_label = ttk.Label(master=cut_month, textvariable=self.slider_data_month)
        month_slider_label.pack()

        # Фрейм кнопок
        test_btn_frame = ttk.LabelFrame(self.test_tab, text='Actions:')
        test_btn_frame.pack(fill=X, padx=(5, 5), pady=(5, 5))
        test_btn_make_graph = ttk.Button(master=test_btn_frame, text='Create Graph', command=self.create_test_graph)
        test_btn_make_graph.pack(pady=(10, 10))
        self.test_btn_save_graph = ttk.Button(master=test_btn_frame, text='Save Graph', command=self.save_test_graph)
        self.test_btn_save_graph.config(state='disabled')
        self.test_btn_save_graph.pack(pady=(0, 10))

        # Фрейм теста отклонения
        test_frame_data = ttk.LabelFrame(self.test_tab, text='Prediction deviations data:')
        test_frame_data.pack(fill=BOTH)
        test_data = ttk.Label(test_frame_data, textvariable=self.predict_data_label)
        test_data.pack(side=LEFT)

        # Вкладка Predict
        self.predict_tab = ttk.Frame(self.notebook, padding=10)
        # Фрейм выбора количества месяцев для предсказания
        predict_month = ttk.LabelFrame(master=self.predict_tab, text='Predict Month:')
        predict_month.pack(fill=X)
        # Слайдер количества месяцев
        month_predict_slider = ttk.Scale(master=predict_month, orient=HORIZONTAL, from_=1, to=100,
                                         command=self.slider_predict)
        month_predict_slider.pack(fill=X, padx=(10, 10), pady=(10, 10))
        month_predict_slider_label = ttk.Label(master=predict_month, textvariable=self.slider_month_predict)
        month_predict_slider_label.pack()
        # Фрейм кнопок
        btn_predict_frame = ttk.LabelFrame(self.predict_tab, text='Action:')
        btn_predict_frame.pack(fill=X, padx=(5, 5), pady=(5, 5))
        btn_predict_graph = ttk.Button(btn_predict_frame, text='Create Graph', command=self.create_predict_graph)
        btn_predict_graph.pack(pady=(10, 10))
        btn_predict_save_graph = ttk.Button(btn_predict_frame, text='Save Graph', command=self.save_predict_graph)
        btn_predict_save_graph.pack(pady=(5, 5))
        btn_predict_save_graph.config(state='disabled')

        self.notebook.add(settings_tab, text='Settings')
        self.notebook.add(self.test_tab, state='disabled', text='Test')
        self.notebook.add(self.predict_tab, state='disabled', text='Predict')

    def result(self):
        self.result_frame = ttk.LabelFrame(master=self, text='Result:')
        self.result_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 20), pady=(0, 20))
        data_show_label = ttk.Label(master=self.result_frame, text='Label', textvariable=self.read_file_data)
        data_show_label.pack(fill=BOTH, side=TOP)

    # Функции обработки
    def open_file(self):
        type_file = (
            ('data files', '*.xls *.xlsx'),
            ('All files', '*.xlsx')
        )
        path = askopenfilename(title="Browse file", filetypes=type_file)
        if path:
            self.path_var.set(path)

    def read_file(self):
        data = database.Data(self.path_var.get())
        self.read_file_data.set(data.get_raw_data)
        self.file_info.set(data.get_frame_size)
        if self.file_info.get():
            self.notebook.add(self.test_tab, state='normal')
            self.notebook.add(self.predict_tab, state='normal')
            self.month_slider.config(from_=1, to=int(self.file_info.get()))

    def change_theme(self, data: str):
        self.style = Style(data.lower())

    def slider_data(self, data):
        self.slider_data_month.set(f"{float(data):.0f}")

    def slider_predict(self, data):
        self.slider_month_predict.set(f"{float(data):.0f}")

    def create_test_graph(self):
        test_data = Data(self.path_var.get(), tail=int(self.slider_data_month.get()))
        all_test_data = Data(self.path_var.get())
        predict_month = MakeFrame.result(PredictMonth.month(test_data.get_last_date, int(self.slider_data_month.get())))
        prophet_data = ProphetDataPredict(test_data.get_data_no_tail, predict_month)
        error_predict = TestPredict(test_data.get_data_tail, prophet_data.predict)

        temp_data_to_label = ''
        for data in error_predict.error_list:
            temp_data_to_label += str(data[0]) + ' ' + str(data[1])[:10] + '%' + '\n'

        self.predict_data_label.set(temp_data_to_label)
        self.read_file_data.set('')

        test_graph = Plot(all_test_data.get_data_no_tail, prophet_data.predict)
        self.clear_plot_canvas(test_graph)

    def create_predict_graph(self):
        actual_data = Data(self.path_var.get())
        predict_month_frame = MakeFrame.result(PredictMonth.month(actual_data.get_last_date,
                                               int(self.slider_month_predict.get())))
        predict_data = ProphetDataPredict(actual_data.get_data_no_tail, predict_month_frame)

        predict_graph = Plot(actual_data.get_data_no_tail, predict_data.predict, True)
        self.clear_plot_canvas(predict_graph)

    def clear_plot_canvas(self, graph):
        self.plot_canvas.get_tk_widget().destroy()
        self.plot_canvas = FigureCanvasTkAgg(graph.draw(self.style.theme_use()), master=self.result_frame)
        self.plot_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True, padx=(5, 5), pady=(5, 5))
        self.plot_canvas.draw()

    def save_test_graph(self):
        pass

    def save_predict_graph(self):
        pass


if __name__ == "__main__":
    App().mainloop()
