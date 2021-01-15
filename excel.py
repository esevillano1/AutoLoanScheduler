import xlwt
from xlwt import Workbook


class ExcelSpreadSheet(Workbook):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.starting_column = 0
        self.ending_column = 0

    def add_new_sheet(self, title):
        self.add_sheet(title)

    def read_txt_file(self, file, mode):
        txt_file = open(file, mode)
        file_line = txt_file.readline().replace("\n", "")
        while file_line != "": 
            self.columns.append(file_line)
            file_line = txt_file.readline().replace("\n", "")
        txt_file.close()

    def set_column_header_range(self):
        self.starting_column = 1
        self.ending_column = self.columns.__len__() + 1


if __name__ == "__main__":
    xlsxSheet = ExcelSpreadSheet()
    sheetName = input("Enter a name for your sheet: ")
    xlsxSheet.add_new_sheet(sheetName)
    xlsxSheet.read_txt_file("columns.txt", "r")
