# Vehicle Trip Calculator

Калькулятор расхода топлива, стоимости и времени поездки для трёх типов
автомобилей с графическим интерфейсом.

## Описание

Приложение рассчитывает для трёх типов транспортных средств:

- **Легковой** — зависимость расхода от массы багажа и пассажиров
- **Грузовой** — зависимость расхода от массы груза
- **Пассажирский (автобус)** — зависимость расхода от числа пассажиров

Для каждой поездки вычисляется:

- расход топлива (л/100 км) с учётом загрузки
- объём необходимого топлива (л)
- стоимость поездки (₽)
- время в пути (ч)

Результаты можно сохранить в отчёт формата `.docx` или `.xlsx`.

## Архитектура

Проект реализован на ООП:

- абстрактный базовый класс `Vehicle` с методами `@abstractmethod`
- иерархия наследования: `Vehicle` → `PassengerCar`, `Truck`, `Bus`
- managed-атрибуты через `@property` и сеттеры с валидацией
- dunder-методы: `__str__`, `__repr__`, `__eq__` у автомобилей,
  `__len__`, `__iter__`, `__repr__` у отчёта

## Структура проекта
algoritms_theory_lab2/
├── vehicles.py # абстрактный класс Vehicle
├── car_types.py # PassengerCar, Truck, Bus
├── reports.py # TripReport — формирование и экспорт отчёта
├── gui.py # графический интерфейс (Tkinter)
├── main.py # консольная версия
├── tests/
│ └── test_all.py # тесты pytest
├── requirements.txt
└── README.md

## Требования

- Python 3.10 или выше
- Tkinter (входит в стандартную поставку Python с python.org;
  для Homebrew-версии требуется `brew install python-tk@3.12`)

## Установка

Клонируйте проект и перейдите в его папку:

```bash
cd algoritms_theory_lab2

Создайте и активируйте виртуальное окружение:
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

## Запуск
```bash
 python gui.py

## Запуск Тестов
```bash
python -m pytest tests/test_all.py -v