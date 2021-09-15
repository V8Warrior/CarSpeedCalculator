from Veh_collector_adaptation import Vehicle
from PyQt5 import QtCore, QtWidgets
from au2 import Ui_MainWindow
import sys

# Create
car = Vehicle()
app = QtWidgets.QApplication([])

# Create Form
form = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(form)
form.show()

#Logic

def button_press():
    car.name_giver(ui.name_in.text()) # Получить имя
    car.rev_param(ui.rpm_in.text()) # Получить обороты
    car.wheel_params(ui.tyres_in.text()) # Получить параметры колес
    car.main_gear_param(ui.main_gear_in.text()) # Получить главную пару
    car.transmission_type(ui.gear_type_in.text()) # Получить тип коробки
    car.gears(ui.gear_ratio_in.text()) # Получить передачи
    car.speed_result()
    data_speed = str(car.speed_data())
    data_car = str(car)
    ui.result_list_out_speed.setText(data_speed)
    ui.result_list_out_chars.setText(data_car)
def save_conf():
    car.name_giver(ui.name_in.text())  # Получить имя
    car.rev_param(ui.rpm_in.text())  # Получить обороты
    car.wheel_params(ui.tyres_in.text())  # Получить параметры колес
    car.main_gear_param(ui.main_gear_in.text())  # Получить главную пару
    car.transmission_type(ui.gear_type_in.text())  # Получить тип коробки
    car.gears(ui.gear_ratio_in.text())  # Получить передачи
    car.config_saver()
def loader_conf():

    car.config_loader()
    ui.result_list_out_chars.setText(str(car))
    pass


def showDialog():
    text, ok = QtWidgets.QInputDialog.getText('Input Dialog',
                                              'Enter your name:')
    if ok:
        ui.name_in.setText(str(text))

ui.result_list_out_chars.setText(str(car))
#
ui.pushButton_result.clicked.connect( button_press )
# ui.pushButton_wheel_help.clicked.connect()
ui.action_4.triggered.connect(save_conf)
# ui.action_3.triggered.connect(showDialog)

# Exit
app.exec()
# car = Vehicle()

# def button_press():
#     app.result_list_out.setText('проверка')
# app.
    # click(button_press())

