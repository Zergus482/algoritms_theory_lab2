import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

from car_types import PassengerCar, Truck, Bus
from reports import TripReport


class VehicleApp(tk.Tk):
    VEHICLES = {
        "Легковой":      PassengerCar,
        "Грузовой":      Truck,
        "Пассажирский":  Bus,
    }

    def __init__(self):
        super().__init__()
        self.title("Калькулятор автомобильных поездок")
        self.geometry("900x600")
        self.minsize(800, 500)
        self.vehicles = {name: cls() for name, cls in self.VEHICLES.items()}
        self.report = TripReport()
        self._build_ui()

    def _build_ui(self):
        top = ttk.LabelFrame(self, text="Автомобиль", padding=10)
        top.pack(fill="x", padx=10, pady=5)
        self.vehicle_var = tk.StringVar(value="Легковой")
        for i, name in enumerate(self.VEHICLES):
            ttk.Radiobutton(top, text=name, value=name,
                            variable=self.vehicle_var,
                            command=self._on_vehicle_change
                            ).grid(row=0, column=i, padx=10, sticky="w")

        params = ttk.LabelFrame(self, text="Параметры поездки", padding=10)
        params.pack(fill="x", padx=10, pady=5)
        ttk.Label(params, text="Дистанция, км:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.distance_var = tk.StringVar(value="100")
        ttk.Entry(params, textvariable=self.distance_var, width=15).grid(row=0, column=1, sticky="w")
        ttk.Label(params, text="Загрузка:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.load_var = tk.StringVar(value="0")
        ttk.Entry(params, textvariable=self.load_var, width=15).grid(row=0, column=3, sticky="w")
        ttk.Label(params, text="Цена топлива, ₽/л:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.price_var = tk.StringVar(value="60")
        ttk.Entry(params, textvariable=self.price_var, width=15).grid(row=1, column=1, sticky="w")
        self.hint_label = ttk.Label(params, text="", foreground="gray")
        self.hint_label.grid(row=1, column=2, columnspan=2, sticky="w", padx=5)

        btns = ttk.Frame(self, padding=5)
        btns.pack(fill="x", padx=10)
        ttk.Button(btns, text="Рассчитать и добавить", command=self._calculate).pack(side="left", padx=5)
        ttk.Button(btns, text="Очистить отчёт", command=self._clear_report).pack(side="left", padx=5)
        ttk.Button(btns, text="Сохранить .docx", command=lambda: self._save("docx")).pack(side="left", padx=5)
        ttk.Button(btns, text="Сохранить .xlsx", command=lambda: self._save("xlsx")).pack(side="left", padx=5)

        table_frame = ttk.LabelFrame(self, text="Результаты", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        cols = ("vehicle", "distance", "load", "consumption", "fuel", "cost", "time")
        headers = ("Автомобиль", "Дистанция, км", "Загрузка",
                   "Расход, л/100км", "Топливо, л", "Стоимость, ₽", "Время, ч")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c, h in zip(cols, headers):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=110, anchor="center")
        self.tree.column("vehicle", width=150)
        self.tree.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=sb.set)

        self.status = tk.StringVar(value="Готово")
        ttk.Label(self, textvariable=self.status, relief="sunken", anchor="w").pack(
            fill="x", side="bottom")
        self._on_vehicle_change()

    def _on_vehicle_change(self):
        v = self.vehicles[self.vehicle_var.get()]
        unit = "пассажиров" if isinstance(v, Bus) else "тонн"
        self.hint_label.config(
            text=f"макс. загрузка: {v.load_capacity} {unit}, "
                 f"база: {v.base_consumption} л/100км")
        self.price_var.set(str(v.fuel_price))
        self.load_var.set("0")

    def _calculate(self):
        v = self.vehicles[self.vehicle_var.get()]
        try:
            distance = float(self.distance_var.get().replace(",", "."))
            load = float(self.load_var.get().replace(",", "."))
            price = float(self.price_var.get().replace(",", "."))
            if distance <= 0:
                raise ValueError("Дистанция должна быть > 0")
            if load < 0 or load > v.load_capacity:
                raise ValueError(f"Загрузка должна быть в диапазоне 0..{v.load_capacity}")
            v.fuel_price = price
            self.tree.insert("", "end", values=(
                v.name, f"{distance:.1f}", f"{load:.2f}",
                f"{v.consumption(load):.2f}", f"{v.fuel_needed(distance, load):.2f}",
                f"{v.trip_cost(distance, load):.2f}", f"{v.trip_time(distance, load):.2f}"))
            self.report.add(v, distance, load)
            self.status.set(f"Добавлено: {v.name}, {distance} км")
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))

    def _clear_report(self):
        if len(self.report) == 0:
            self.status.set("Отчёт уже пуст")
            return
        if messagebox.askyesno("Подтверждение", "Очистить все результаты?"):
            for i in self.tree.get_children():
                self.tree.delete(i)
            self.report = TripReport()
            self.status.set("Отчёт очищен")

    def _save(self, fmt: str):
        if len(self.report) == 0:
            messagebox.showwarning("Нет данных", "Сначала добавьте хотя бы одну поездку")
            return
        ext = ".docx" if fmt == "docx" else ".xlsx"
        path = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=[("Word" if fmt == "docx" else "Excel", f"*{ext}")],
            initialfile=f"report{ext}")
        if not path:
            return
        try:
            (self.report.to_docx if fmt == "docx" else self.report.to_xlsx)(path)
            self.status.set(f"Сохранено: {os.path.basename(path)}")
            messagebox.showinfo("Успех", f"Файл сохранён:\n{path}")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))


def main():
    app = VehicleApp()
    app.mainloop()


if __name__ == "__main__":
    main()