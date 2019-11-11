import xlrd
import xlwt
import os


class XlsReader:
    def __init__(self, file: str):
        self.file_path = file

    def read_data(self, n:int = 0):
        try:
            wb = xlrd.open_workbook(self.file_path)
            sheet = wb.sheet_by_index(0)
            result_list = []
            for nr in range(n, sheet.nrows):
                row = sheet.row(nr)
                cells = []
                for cell in row:
                    cell = str(cell).replace("'", "").split(":")
                    cells.append((cell[0], ":".join(cell[1:])))
                result_list.append(cells)
            return result_list
        except Exception:
            return None


class XlsWriter:
    def __init__(self, file: str):
        if os.path.exists(file):
            os.remove(file)
        self.file_path = file
        self.sheets = []
        self.tables = []
        self.wb = xlwt.Workbook()

    def add_sheet(self, text, table: list):
        header_font = xlwt.Font()
        header_font.bold = True

        header_style = xlwt.XFStyle()
        header_style.font = header_font

        ws = self.wb.add_sheet(text)
        if len(table) > 0:
            for c in range(len(table[0])):
                ws.write(0, c, table[0][c], header_style)

        if len(table) > 1:
            for r in range(1, len(table)):
                for c in range(len(table[r])):
                    ws.write(r, c, table[r][c])

    def save(self):
        self.wb.save(self.file_path)
