from xlrd import open_workbook


class readExcel():
    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name    # 用于获取case表

    def get_file(self):# xls_name填写用例的Excel名称 sheet_name该Excel的sheet名称
        file = open_workbook(self.file_path)# 打开用例Excel
        return file

    def get_parametrize(self):
        parametrize = []
        f = self.get_file()
        sheet = f.sheet_by_name(self.sheet_name)  # 获得打开Excel的sheet

        nrows = sheet.nrows         # 获取这个sheet内容行数
        for i in range(1, nrows):   # 跳过第一行
            parametrize.append(sheet.row_values(i))

        return parametrize