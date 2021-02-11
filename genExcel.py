import xlsxwriter

class mainExcel():

	# generate main workbook
	def __init__(self, fname):
		self.workbook = xlsxwriter.Workbook('%s.xlsx' % fname)

		# set formating
		self.bold = self.workbook.add_format({'bold':True})


	# generate sheet and insert columns and data
	def sheet(self, sname, columns, data):

		# generate sheet
		self.worksheet = self.workbook.add_worksheet(sname)

		# insert columns
		for c in range(len(columns)):
			self.worksheet.write(0, c, columns[c], self.bold)

		# insert data
		for rc, rd in enumerate(data): # itterate over each row
			for i, d in enumerate(rd): # itterate over each data
				self.worksheet.write(rc+1, i, d)


	# close workbook
	def close(self):
		self.workbook.close()


if __name__ == "__main__":

	# prepare variables
	SHEET_ = "Names" 
	HEADER_ = ['Full Name','Count','Mobile']
	DATA_ = [
		['Ricky','12','ricky@gmail.com'],
		['Mark','23','mark@nta.ac.in'],
		['Steve','98','steve@jobs.com']
	]

	m = mainExcel('hp')
	sheet_1 = m.sheet(SHEET_, HEADER_, DATA_)
	m.close()
