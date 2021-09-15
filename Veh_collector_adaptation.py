import re
import pandas as pd
import numpy as np
import json
import os.path


def string_cleaner(text, reg=r'\w+'):
    compiled = re.compile(reg)
    res = compiled.findall(text)
    return res

class Vehicle:
    def __init__(self, name='Х'):
        self.name = name
        self.rpm = 'Не указаны'
        self.wheels = 'Не указаны'
        self.transmission = 'Не указана'
        self.kpd_gearing = .9
        self.kpd_maingear = .96
        self.main_gear = 'Не указана'
        self.gear_nums = 'Не указано'
        self.geardict = None
        self.speeddict = None

    def __str__(self):
        return f'Состояние машины:\n ' \
               f'Имя : {self.name} \n ' \
               f'Обороты: {self.rpm} \n ' \
               f'Парметры колес: {self.wheels} \n ' \
               f'Тип КПП: {self.transmission} \n ' \
               f'Количество передач: {self.gear_nums} \n ' \
               f'Главная пара: {self.main_gear} \n'

    def name_giver(self, name=None):
        if name != None:
            self.name = name
        else:
            new_name = ' '.join(string_cleaner(input()))
            if new_name != '':
                self.name = new_name
            else:
                return '\n Имя содержит только недопустимые знаки, ввод не удался \n'

    def rev_param(self, rpms='Не указаны'):
        rpms = str(rpms)
        rpms = string_cleaner(rpms, r'\d+')
        if len(rpms) != 0:
            rpms = ''.join(rpms)
            self.rpm = int(rpms)
            return rpms
        else:
            return '\nНеверное значение, ввод не удался\n'

    def wheel_params(self, wheel='Не указаны'):
        wheel = str(wheel)
        whl_list = string_cleaner(wheel, r'\d+')
        if len(whl_list) == 3:
            whl_dict = {'wide': int(whl_list[0]), 'profile': int(whl_list[1]), 'diameter': int(whl_list[2])}
            self.wheels = whl_dict
            return whl_dict
        else:
            return '\nНекорректные параметры, ввод не удался\n'

    def transmission_type(self, gear='Не указана'):
        gear = str(gear)
        if gear.isalpha() == True:
            gear = gear.lower()
            if gear.__contains__('m') or gear.__contains__('м'):
                self.transmission = 'Механика'
                self.kpd_gearing = .9
            elif gear.__contains__('a') or gear.__contains__('а'):
                self.transmission = 'Автомат'
                self.kpd_gearing = .82
            elif gear.__contains__('v') or gear.__contains__('в'):
                self.transmission = 'Вариатор'
                self.kpd_gearing = .85
            elif gear.__contains__('r') or gear.__contains__('р'):
                self.transmission = 'Робот'
                self.kpd_gearing = .88
            else:
                return '\nНет такого типа коробки\n'
        else:
            return '\nНеверное значение, ввод не удался\n'

    def main_gear_param(self, mg='Не указана'):
        mg = str(mg)
        mg = string_cleaner(mg)
        if ''.join(mg).isdigit() == True:
            gear = float('.'.join(mg))
            if gear != 0:
                self.main_gear = gear
                return mg
        else:
            return '\nНеверное значение, ввод не удался\n'

    def gears(self, gears='Не указаны'):
        gears = str(gears)
        gearlist = gears.split(' ')
        clean_list = []
        for gear in gearlist:
            cleaned = string_cleaner(gear, r'\d+')
            if len(cleaned) != 0:
                cleaned = float('.'.join(cleaned))
                if cleaned != 0:
                    clean_list.append(cleaned)
        geardict = {}

        for i, gear in enumerate(clean_list):
            geardict[i + 1] = float(gear)
        self.gear_nums = len(geardict.keys())
        self.geardict = geardict


        # else:
        #     print('\nНеверное значение, ввод не удался\n')

    def gear_data(self):
        frame = pd.DataFrame([self.geardict])
        if type(self.main_gear) != 'str':
            frame['main'] = self.main_gear
        return frame

    def config_saver(self):
        d = {
            'name': self.name,
            'rpm': self.rpm,
            'wheels': self.wheels,
            'gear_type': self.transmission,
            'gear_count': self.gear_nums,
            'kpd_gear': self.kpd_gearing,
            'axle_gear': self.main_gear
        }
        for key, value in self.geardict.items():
            d[key] = value
        data = json.dumps(d)
        with open(self.name + '_configer.json', 'w') as file:
            json.dump(data, file)
        print('Сохранение завершено')
        return data

    def config_loader(self, name):
        fname = f'{name}_configer.json'
        if os.path.exists(fname):
            with open(fname, 'r') as file:
                frame = json.loads(json.load(file))

                self.name = frame['name']
                self.rpm = frame['rpm']
                self.wheels = frame['wheels']
                self.transmission = frame['gear_type']
                self.gear_nums = frame['gear_count']
                self.kpd_gearing = frame['kpd_gear']
                self.main_gear = frame['axle_gear']
                if len(frame.keys()) > 7:
                    self.geardict = {}

                    for i in list(frame.keys())[7:]:
                        self.geardict[i] = frame[i]

        else:
            return 'Машина не найдена'

    def speed_result(self):
        if isinstance(self.rpm, int):
            if isinstance(self.main_gear, float):
                if isinstance(self.wheels, dict):
                    if isinstance(self.geardict, dict):
                        speeddict = {}
                        roll_rad = 0.012 * self.wheels['diameter'] \
                                   + 0.00001 * self.wheels['profile'] * self.wheels['wide']

                        for i, gear in self.geardict.items():
                            speed = 0.377 * roll_rad * self.rpm / (gear * self.main_gear)
                            speeddict[i] = round(speed, 2)

                        self.speeddict = speeddict
                        return speeddict
                    else:
                        return 'Отсутствуют значения Передаточных Отношений Коробки'
                else:
                    return 'Отсутствуют значения Параметров Шин'
            else:
                return 'Отсутствует значение Главной Пары'
        else:
            return 'Отсутствует значение Оборотов'

    def speed_data(self):
        if self.speeddict != None:
            speedlist = []
            for key, value in self.speeddict.items():
                speedlist.append([key, value])
            frame = pd.DataFrame(speedlist, columns=['gear', 'km/h']).set_index('gear')
            return frame
        else:
            return 'Нет всех данных'

# car = Vehicle()
# car.speed_result()
# print(car.speed_data())

