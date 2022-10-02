from typing import Dict, Type, ClassVar
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: str
    duration: float
    weight: float

    M_IN_KM: ClassVar[int] = 1000  # const
    LEN_STEP: ClassVar[float] = 0.65
    D_IN_M: ClassVar[int] = 60

    def get_distance(self):
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self):  # Значение средней скорости
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        training_info = InfoMessage(type(self).__name__, self.duration,
                                    self.get_distance(),
                                    self.get_mean_speed(),
                                    self.get_spent_calories())
        return training_info


class Running(Training):
    """Тренировка: бег."""
    CF_CL_1: ClassVar[int] = 18
    CF_CL_2: ClassVar[int] = 20

    def get_spent_calories(self):
        spent_calories = ((self.CF_CL_1 * self.get_mean_speed()
                           - self.CF_CL_2)
                          * self.weight / self.M_IN_KM * self.duration
                          * self.D_IN_M)
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CEF_CLRS_1: ClassVar[float] = 0.035
    CEF_CLRS_2: ClassVar[float] = 0.029

    action: str
    duration: float
    weight: float
    height: float

    def get_spent_calories(self):
        spent_calories = ((self.CEF_CLRS_1 * self.weight
                           + (self.get_mean_speed()
                              ** 2 // self.height) * self.CEF_CLRS_2
                           * self.weight)
                          * self.duration * self.D_IN_M
                          )
        return spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_mean_speed(self):
        average_speed = (self.length_pool * self.count_pool / self.M_IN_KM
                         / self.duration)
        return average_speed

    def get_spent_calories(self):
        spent_calories = ((self.get_mean_speed() + 1.1)
                          * 2 * self.weight)
        return spent_calories


def read_package(workout: str, all_data: list):
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking,
    }
    if workout not in training_type:
        raise NameError('Сообщение об ошибке')
    else:
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