from typing import Tuple
from docx import Document
from openpyxl import Workbook
from vehicles import Vehicle           


TripRow = Tuple[Vehicle, float, float, float, float, float]


class TripReport:
    def __init__(self):
        self._rows: list[TripRow] = []

    def add(self, vehicle: Vehicle, distance: float, load: float):
        self._rows.append((
            vehicle,
            distance,
            load,
            vehicle.consumption(load),
            vehicle.fuel_needed(distance, load),
            vehicle.trip_cost(distance, load),
            vehicle.trip_time(distance, load),
        ))

    def __len__(self) -> int:
        return len(self._rows)

    def __iter__(self):
        return iter(self._rows)

    def __repr__(self) -> str:
        return f"TripReport(rows={len(self._rows)})"

    def to_docx(self, path: str) -> str:
        doc = Document()
        doc.add_heading("Отчёт: расчёт поездок", level=1)
        table = doc.add_table(rows=1, cols=7)
        table.style = "Light Grid Accent 1"
        hdr = table.rows[0].cells
        headers = ["Автомобиль", "Дистанция, км", "Загрузка",
                   "Расход, л/100км", "Топливо, л", "Стоимость, ₽", "Время, ч"]
        for i, h in enumerate(headers):
            hdr[i].text = h

        for v, d, l, c, f, cost, t in self._rows:
            r = table.add_row().cells
            r[0].text = str(v)
            r[1].text = f"{d:.1f}"
            r[2].text = f"{l:.2f}"
            r[3].text = f"{c:.2f}"
            r[4].text = f"{f:.2f}"
            r[5].text = f"{cost:.2f}"
            r[6].text = f"{t:.2f}"

        doc.save(path)
        return path

    def to_xlsx(self, path: str) -> str:
        wb = Workbook()
        ws = wb.active
        ws.title = "Поездки"
        ws.append(["Автомобиль", "Дистанция, км", "Загрузка",
                   "Расход, л/100км", "Топливо, л", "Стоимость, ₽", "Время, ч"])
        for v, d, l, c, f, cost, t in self._rows:
            ws.append([str(v), d, l, round(c, 2), round(f, 2),
                       round(cost, 2), round(t, 2)])
        wb.save(path)
        return path