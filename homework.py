class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,  # имя класса тренировки;
                 duration: float,  # длительность тренировки в часах
                 distance: float,  # дистанция в км.
                 speed: float,  # средняя скорость движения пользователя
                 calories: float  # количество потраченных ккал
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000  # метров в одном км
    LEN_STEP: float = 0.65  # метров в одном шаге

    def __init__(self,
                 action: int,  # число движений
                 duration: float,  # продолжительность
                 weight: float  # масса
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: int = self.action * self.LEN_STEP / self.M_IN_KM
        # вычисление дистанции
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        # вычисление средней скорости
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # этот метод будет переопределяться в дочерних классах
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    minute: int = 60  # минуты
    coeff_calorie_run1: int = 18  # Коэфициент каллорий 1
    coeff_calorie_run2: int = 20  # Коэфициент каллорий 2

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.coeff_calorie_run1 * self.get_mean_speed()
                    - self.coeff_calorie_run2) * self.weight / self.M_IN_KM
                    * (self.duration * self.minute))
        # переопределенный метод для бега
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    minute: int = 60  # минуты
    coeff_calorie_wlk1: float = 0.035  # Коэфициент калорий 1
    coeff_calorie_wlk2: float = 0.029  # Коэфициент калорий 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int  # рост
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.coeff_calorie_wlk1 * self.weight
                    + (self.get_mean_speed() ** 2 // self.height)
                    * self.coeff_calorie_wlk2 * self.weight) * (self.duration
                    * self.minute))
        # переопределенный метод для ходьбы
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_calorie_swm1: float = 1.1  # Коэфициент калорий 1
    coeff_calorie_swm2: int = 2  # Коэфициент калорий 2
    LEN_STEP: float = 1.38  # метров в одном гребке

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,  # длина бассейна в метрах;
                 count_pool: int  # число преодолений бассейна
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.get_mean_speed() + self.coeff_calorie_swm1)
                    * self.coeff_calorie_swm2 * self.weight)
        # переопределенный метод для плавания
        return calories

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        # переопределенный метод для плавания
        return mean_speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
