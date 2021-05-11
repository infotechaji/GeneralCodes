

import openpyxl


def write_excel(work_book_name, rows=[]):
	book = openpyxl.load_workbook(work_book_name)
	sheet = book.active
	for row in rows:
		sheet.append(row)
		book.save(work_book_name)
	return True


if __name__ == "__main__":
	work_book_name = 'appending.xlsx'
	rows = [
	    [88, 46, 57],
	    [89, 38, 12],
	    [23, 59, 78],
	    [56, 21, 98],
	    [24, 18, 43],
	    [34, 15, 67]
	]
	for i in range(5):
		write_excel(work_book_name,rows = rows)