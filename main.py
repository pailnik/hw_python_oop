from typing import Dict, Type
M_IN_KM = 1000  # const
coeff_calorie_1 = 18
coeff_calorie_2 = 20
cef_call_1 = 0.035
cef_call_2 = 0.029


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср.скорость: {self.speed:.3f} км / ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65

    def __init__(self, action, duration, weight):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self):
        dist = self.action * self.LEN_STEP / M_IN_KM  # Dopisat vubor LEN
        return dist

    def get_mean_speed(self):  # Значение средней скорости
        average_speed = Training.get_distance(self) / self.duration
        return average_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        training_info = InfoMessage(self.__class__.__name__, self.duration,
                                    self.get_distance(), self.get_mean_speed(),
                                    self.get_spent_calories())
        return training_info


class Running(Training):
    """def __init__(self, action, duration, weight, average_speed):
        super().__init__(action, duration, weight)
        self.average_speed = Training.get_mean_speed(self, duration)

    def get_spent_calories(self, weight):
        spent_calories = ((coeff_calorie_1 * self.average_speed - coeff_calorie_2)
                          * self.weight / M_IN_KM * self.duration)
        return spent_calories"""

    def get_spent_calories(self):
        spent_calories = ((coeff_calorie_1 * Training.get_mean_speed(self) - coeff_calorie_2)
                          * self.weight / M_IN_KM * self.duration)
        return spent_calories


class SportsWalking(Training):
    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        minute = 60
        spent_calories = ((cef_call_1 * self.weight +
                         (Training.get_mean_speed(self)
                         ** 2 // self.height) * cef_call_2 * self.weight)
                         * self.weight
                         * self.duration * minute  # v minutah
                          )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        average_speed = self.length_pool * self.count_pool / M_IN_KM / self.duration
        return average_speed

    def get_spent_calories(self):
        spent_calories = ((Swimming.get_mean_speed(self) + 1.1)
                          * 2 * self.weight)
        return spent_calories


def read_package(workout: str, all_data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking,
    }
    return training_type[workout](*all_data)


def main(user_training: Training) -> None:
    """Главная функция."""
    info = user_training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [        
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
