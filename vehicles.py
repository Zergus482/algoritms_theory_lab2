from abc import ABC, abstractmethod


class Vehicle(ABC):
    """Абстрактный автомобиль."""

    FUEL_PRICE = 60.0  # руб/литр — managed-атрибут класса (можно менять)

    def __init__(self, name: str, base_consumption: float,
                 load_capacity: float, fuel_price: float | None = None):
        self.name = name
        self.base_consumption = base_consumption   # л/100км расход
        self.load_capacity = load_capacity         # тонн или мест
        self.fuel_price = fuel_price if fuel_price is not None else self.FUEL_PRICE

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя должно быть непустой строкой")
        self._name = value.strip()

    @property
    def base_consumption(self) -> float:
        return self._base_consumption

    @base_consumption.setter
    def base_consumption(self, value: float):
        if value <= 0:
            raise ValueError("Базовый расход должен быть > 0")
        self._base_consumption = value

    @property
    def load_capacity(self) -> float:
        return self._load_capacity

    @load_capacity.setter
    def load_capacity(self, value: float):
        if value <= 0:
            raise ValueError("Грузоподъёмность/вместимость должна быть > 0")
        self._load_capacity = value

    @property
    def fuel_price(self) -> float:
        return self._fuel_price

    @fuel_price.setter
    def fuel_price(self, value: float):
        if value <= 0:
            raise ValueError("Цена топлива должна быть > 0")
        self._fuel_price = value


    @abstractmethod
    def consumption(self, load: float) -> float:
        """Расход л/100км с учётом загрузки."""
        raise NotImplementedError

    @abstractmethod
    def avg_speed(self, load: float) -> float:
        """Средняя скорость км/ч с учётом загрузки."""
        raise NotImplementedError

    def fuel_needed(self, distance: float, load: float) -> float:
        if distance <= 0:
            raise ValueError("Дистанция должна быть > 0")
        return self.consumption(load) * distance / 100

    def trip_cost(self, distance: float, load: float) -> float:
        return self.fuel_needed(distance, load) * self._fuel_price

    def trip_time(self, distance: float, load: float) -> float:
        if distance <= 0:
            raise ValueError("Дистанция должна быть > 0")
        return distance / self.avg_speed(load)

    def __str__(self) -> str:
        return (f"{self.name} (база {self._base_consumption} л/100км, "
                f"вместимость {self._load_capacity})")

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(name={self._name!r}, "
                f"base_consumption={self._base_consumption}, "
                f"load_capacity={self._load_capacity})")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vehicle):
            return NotImplemented
        return (self.__class__ is other.__class__
                and self._base_consumption == other._base_consumption
                and self._load_capacity == other._load_capacity)