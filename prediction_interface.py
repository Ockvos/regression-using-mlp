from tkinter import *
import pandas as pd
import tkinter
import datetime


class PredictionInterface:

    def __init__(self):

        self.y_scaler = None
        self.x_scaler = None
        self.trained_model = None
        self.prediction_label = None


        self.diamond_cut = {'Ideal': 5, 'Premium': 4, 'Very Good': 3, 'Good': 2, 'Fair': 1}
        self.diamond_clarity = dict(IF=11, VVS1=10, VVS2=9, VS1=8, VS2=7, SI1=6, SI2=5, I1=3)
        self.diamond_colors = dict(D=23, E=22, F=21, G=20, H=19, I=18, J=17)


        self.user_numeric_inputs = dict(carat="N/A", x="N/A", y="N/A", z="N/A", depth="N/A", table="N/A")
        self.user_category_inputs = dict(cut="N/A", clarity="N/A", color="N/A")

        self.font_type = "Arial"
        self.font_size = 12


    def set_x_scaler(self, x_scaler):
        self.x_scaler = x_scaler

    def set_y_scaler(self, y_scaler):
        self.y_scaler = y_scaler

    def set_trained_model(self, trained_model):
        self.trained_model = trained_model

    def run_prediction(self):

        if "N/A" in self.user_numeric_inputs.values():
            return
        if "N/A" in self.user_category_inputs.values():
            return
        try:  # Prevent value errors
            carat = float(self.user_numeric_inputs.get("carat"))
            x = float(self.user_numeric_inputs.get("x"))
            y = float(self.user_numeric_inputs.get("y"))
            z = float(self.user_numeric_inputs.get("z"))
            depth = float(self.user_numeric_inputs.get("depth"))
            table = float(self.user_numeric_inputs.get("table"))
        except ValueError:
            # Creates and writes to file for any incorrect user inputs
            with open("exceptions_log.txt", "a") as file:
                file.write("VALUE ERROR AT " + str(datetime.datetime.now()) + ": ")
                file.write(str(self.user_numeric_inputs))
                file.write("\n")
                file.close()
            return

        cut = self.diamond_cut.get(self.user_category_inputs.get("cut"))
        clarity = self.diamond_clarity.get(self.user_category_inputs.get("clarity"))
        color = self.diamond_colors.get(self.user_category_inputs.get("color"))

        data = {"carat": [carat],
                "cut": [cut],
                "color": [color],
                "clarity": [clarity],
                "depth": [depth],
                "table": [table],
                "x": [x],
                "y": [y],
                "z": [z]}

        print(data)
        input_values = pd.DataFrame(data)

      #  input_values = [[carat, cut, color, clarity, depth, table, x, y, z]]

        input_values = self.x_scaler.transform(input_values)

        predicted_price = self.trained_model.predict(input_values)

        predicted_price = self.y_scaler.inverse_transform(predicted_price.reshape(-1, 1))

        result = "$" + str(round(predicted_price[0][0], 2))

        self.prediction_label.config(text=result)

    def gather_inputs(self, dictionary, input_name, input_value):
        dictionary.update({input_name: input_value})


    def populate_listbox(self, main_win, name_label, dictionary, box, label_row_loc, label_col_loc, box_row_loc, box_col_loc):
        name_label.grid(row=label_row_loc, column=label_col_loc)
        sorted_dict = sorted(dictionary.items(), key=lambda x: x[1])
        for key in sorted_dict:
            box.insert(END, '{}'.format(key[0]))
        box.grid(row=box_row_loc, column=box_col_loc)
        scrollbar = Scrollbar(main_win, orient=VERTICAL, repeatdelay=900)
        box.config(yscrollcommand=scrollbar.set, exportselection=False)
        scrollbar.config(command=box.yview)
        scrollbar.grid(row=box_row_loc, column=box_col_loc + 1, sticky='ns')

    def launch_interface(self):
        m = tkinter.Tk()  # where m is the name of the main window object

        # Set up the window
        m.title("Diamond Prediction")
        m.geometry("400x900")
        m.minsize(500, 700)
        m.maxsize(500, 700)

        # Carat entry box
        carat_label = Label(m, text='Carat', font=(self.font_type, self.font_size))
        carat_label.grid(row=0, column=0)
        carat_entry = Entry(m, width=20, font=(self.font_type, self.font_size))
        carat_entry.bind("<KeyRelease>",
                         lambda event, arg=0: self.gather_inputs(self.user_numeric_inputs, "carat", carat_entry.get()))
        carat_entry.grid(row=0, column=1)

        # X entry box
        x_label = Label(m, text='X Dimension', font=(self.font_type, self.font_size))
        x_label.grid(row=1, column=0)
        x_entry = Entry(m, width=20, font=(self.font_type, self.font_size))
        x_entry.bind("<KeyRelease>", lambda event, arg=0: self.gather_inputs(self.user_numeric_inputs, "x", x_entry.get()))
        x_entry.grid(row=1, column=1)

        # Y entry box
        y_label = Label(m, text='Y Dimension', font=(self.font_type, self.font_size))
        y_label.grid(row=2, column=0)
        y_entry = Entry(m, width=20, font=(self.font_type, self.font_size))
        y_entry.bind("<KeyRelease>", lambda event, arg=0: self.gather_inputs(self.user_numeric_inputs, "y", y_entry.get()))
        y_entry.grid(row=2, column=1)

        # Z entry box
        z_label = Label(m, text='Z Dimension', font=(self.font_type, self.font_size))
        z_label.grid(row=3, column=0)
        z_entry = Entry(m, width=20, font=(self.font_type, self.font_size))
        z_entry.bind("<KeyRelease>", lambda event, arg=0: self.gather_inputs(self.user_numeric_inputs, "z", z_entry.get()))
        z_entry.grid(row=3, column=1)

        # Depth entry box
        depth_label = Label(m, text='Depth', font=(self.font_type, self.font_size))
        depth_label.grid(row=4, column=0)
        depth_entry = Entry(m, width=20, font=(self.font_type, self.font_size))
        depth_entry.bind("<KeyRelease>",
                         lambda event, arg=0: self.gather_inputs(self.user_numeric_inputs, "depth", depth_entry.get()))
        depth_entry.grid(row=4, column=1)

        # Table entry box
        table_label = Label(m, text='Table', font=(self.font_type, self.font_size))
        table_label.grid(row=5, column=0)
        table_entry = Entry(m, width=20, font=(self.font_type, self.font_size))
        table_entry.bind("<KeyRelease>",
                         lambda event, arg=0: self.gather_inputs(self.user_numeric_inputs, "table", table_entry.get()))
        table_entry.grid(row=5, column=1)

        # Cut choice box
        table_label = Label(m, text='Cut', font=(self.font_type, self.font_size))
        cut_box = Listbox(m, height=5, font=(self.font_type, self.font_size))
        self.populate_listbox(m, table_label, self.diamond_cut, cut_box, 6, 0, 6, 1)
        cut_box.bind("<<ListboxSelect>>",
                     lambda event, arg=0: self.gather_inputs(self.user_category_inputs, "cut", cut_box.get(ANCHOR)))

        # Clarity choice box
        table_label = Label(m, text='Clarity', font=(self.font_type, self.font_size))
        clarity_box = Listbox(m, height=5, font=(self.font_type, self.font_size))
        self.populate_listbox(m, table_label, self.diamond_clarity, clarity_box, 7, 0, 7, 1)
        clarity_box.bind("<<ListboxSelect>>",
                         lambda event, arg=0: self.gather_inputs(self.user_category_inputs, "clarity", clarity_box.get(ANCHOR)))

        # Color choice box
        table_label = Label(m, text='Color', font=(self.font_type, self.font_size))
        color_box = Listbox(m, height=5, font=(self.font_type, self.font_size))
        self.populate_listbox(m, table_label, self.diamond_colors, color_box, 8, 0, 8, 1)
        color_box.bind("<<ListboxSelect>>",
                       lambda event, arg=0: self.gather_inputs(self.user_category_inputs, "color", color_box.get(ANCHOR)))

        # Label stating prediction results
        self.prediction_label = Label(m, font=("Arial", 15), text='Waiting for inputs')
        self.prediction_label.grid(row=10, column=1)

        # The prediction button
        button = tkinter.Button(m, text='Predict', width=16, height=2, bg="light green", font="bold",
                                activebackground="green")
        button.config(command=self.run_prediction)
        button.grid(row=9, column=1)


        m.mainloop()
