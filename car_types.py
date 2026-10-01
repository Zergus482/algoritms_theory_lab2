from vehicles import Vehicle


class PassengerCar(Vehicle):
    """Легковой: 4-5 мест, малая грузоподъёмность."""

    def __init__(self, name: str = "Легковой",
                 base_consumption: float = 7.0,
                 load_capacity: float = 0.4,           # тонн (багаж+пассажиры)
                 fuel_price: float | None = None):
        super().__init__(name, base_consumption, load_capacity, fuel_price)

    def consumption(self, load: float) -> float:
        self._check_load(load)
        # +3% к расходу на каждые 100 кг загрузки
        return self._base_consumption * (1 + 0.03 * (load / 0.1))

    def avg_speed(self, load: float) -> float:
        self._check_load(load)
        # базово 90 км/ч, минус 5 км/ч на каждые 100 кг
        return max(40.0, 90.0 - 5.0 * (load / 0.1))

    def _check_load(self, load: float):
        if load < 0 or load > self._load_capacity:
            raise ValueError(f"Загрузка вне диапазона 0..{self._load_capacity}")

    def __str__(self) -> str:
        return  super().__str__()

    def __repr__(self) -> str:
        return f"PassengerCar(name={self._name!r})"


class Truck(Vehicle):
    """Грузовой: большая грузоподъёмность, сильная зависимость от загрузки."""

    def __init__(self, name: str = "Грузовой",
                 base_consumption: float = 25.0,
                 load_capacity: float = 20.0,          # тонн
                 fuel_price: float | None = None):
        super().__init__(name, base_consumption, load_capacity, fuel_price)

    def consumption(self, load: float) -> float:
        self._check_load(load)
        # +1.5% на каждую тонну
        return self._base_consumption * (1 + 0.015 * load)

    def avg_speed(self, load: float) -> float:
        self._check_load(load)
        # базово 80 км/ч, минус 1.2 км/ч на тонну, минимум 60
        return max(60.0, 80.0 - 1.2 * load)

    def _check_load(self, load: float):
        if load < 0 or load > self._load_capacity:
            raise ValueError(f"Загрузка вне диапазона 0..{self._load_capacity}")

    def __str__(self) -> str:
        return  super().__str__()

    def __repr__(self) -> str:
        return f"Truck(name={self._name!r}, capacity={self._load_capacity})"


class Bus(Vehicle):
    """Пассажирский: загрузка в пассажирах (мест)."""

    def __init__(self, name: str = "Пассажирский",
                 base_consumption: float = 18.0,
                 load_capacity: float = 50.0,          # мест
                 fuel_price: float | None = None):
        super().__init__(name, base_consumption, load_capacity, fuel_price)

    def consumption(self, load: float) -> float:
        self._check_load(load)
        # +0.5% на каждого пассажира
        return self._base_consumption * (1 + 0.005 * load)

    def avg_speed(self, load: float) -> float:
        self._check_load(load)
        # базово 60 км/ч, минус 0.1 км/ч на пассажира
        return max(40.0, 60.0 - 0.1 * load)

    def _check_load(self, load: float):
        if load < 0 or load > self._load_capacity:
            raise ValueError(f"Число пассажиров вне диапазона 0..{self._load_capacity}")

    def __str__(self) -> str:
        return  super().__str__()

    def __repr__(self) -> str:
        return f"Bus(name={self._name!r}, seats={self._load_capacity})"