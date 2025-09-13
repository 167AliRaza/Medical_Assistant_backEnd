import gspread

gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key("1OV_ImyLzqHBBD4PskSj8Q85aoI35PEBYVgC40ZMAu3Q")
worksheet = sh.worksheet("Sheet1")
data = worksheet.get_all_values()



