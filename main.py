from car_types import PassengerCar, Truck, Bus
from reports import TripReport


def input_float(prompt: str, minimum: float | None = None) -> float:
    while True:
        try:
            v = float(input(prompt))
            if minimum is not None and v < minimum:
                print(f"Значение должно быть ≥ {minimum}")
                continue
            return v
        except ValueError:
            print("Введите число!")


def main():
    vehicles = {"1": PassengerCar(), "2": Truck(), "3": Bus()}
    report = TripReport()
    while True:
        print("\n=== Калькулятор поездок ===")
        for k, v in vehicles.items():
            print(f"  {k}. {v}")
        print("4. Отчёт (docx + xlsx)")
        print("0. Выход")
        choice = input("Выбор: ").strip()
        if choice in vehicles:
            v = vehicles[choice]
            try:
                load = input_float(f"Загрузка (0..{v.load_capacity}): ", minimum=0)
                distance = input_float("Дистанция, км: ", minimum=0.1)
                price = input(f"Цена топлива (Enter = {v.fuel_price}): ").strip()
                if price:
                    v.fuel_price = float(price)
                print(f"\n--- {v.name} ---")
                print(f"Расход:    {v.consumption(load):.2f} л/100км")
                print(f"Топливо:   {v.fuel_needed(distance, load):.2f} л")
                print(f"Стоимость: {v.trip_cost(distance, load):.2f} ₽")
                print(f"Время:     {v.trip_time(distance, load):.2f} ч")
                report.add(v, distance, load)
            except ValueError as e:
                print(f"Ошибка: {e}")
        elif choice == "4":
            if len(report) == 0:
                print("Нет данных"); continue
            report.to_docx("report.docx")
            report.to_xlsx("report.xlsx")
            print(f"Сохранено {len(report)} записей")
        elif choice == "0":
            break
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()