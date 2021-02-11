from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, MetaData
import pandas as pd
import os
import hashlib
import datetime
import string

############### FUNCTIONS ####################

def getCorrectColumn(name): # check if all charaters in name is alphanumeric
	n = ""
	l = list(string.ascii_letters)
	d = list(string.digits)
	l.extend(d)

	for c in name:
		if c not in l:
			c = "_"
		n += c

	return n.lower()

def getDividers(): # this function is just a page divider
	print("="*30)

############### DATABASE ####################
 
DB_TYPE_ = "postgresql"
HOST_ = "localhost"
PORT_ = "5432"
DATABASE_ = "data"
USER_ = "ricky"
PASS_ = "749382"
META_ = MetaData()

# DATABASE Connection
db_engine = create_engine(f'{DB_TYPE_}://{USER_}:{PASS_}@{HOST_}:{PORT_}/{DATABASE_}')

# Create directory table
try:
	table_check = db_engine.execute("SELECT * FROM directory")
except:
	directory = Table(
	   'directory', META_, 
	   Column('id', Integer, primary_key = True), 
	   Column('file_name', String), 
	   Column('hash', String),
	)

	META_.create_all(db_engine)

################ FILE FINDER ################

DATA_FOLDER_PATH = "Data"

try:
	# list all file in the folder [Data]
	files = os.listdir(DATA_FOLDER_PATH)

	print("Select the file to upload")

	for c, f in enumerate(files):
		print("%s) %s" % (c, f))

	ii_ = input('Enter the file number (comma seperated for multiple files): ').split(',')

except Exception as e:

	print(str(e))

getDividers()

################ UPLOAD DATA ################

for i in ii_:

	# remove any spaces
	i = i.strip()

	# check if selected file is correct
	if i not in list(string.digits) or int(i) > len(files):

		print(f"{i} : incorrect file selected")

		getDividers()

		pass

	else:

		i = int(i) # convert to integer
		
		# check if file is excel or csv
		selected_file = files[i]
		file_ext = selected_file.split('.')[-1]
		ALLOWED_EXT = ['xlsx', 'xls', 'csv']

		if file_ext not in ALLOWED_EXT:

			print(f"{i} : The selected file format is incorrect")

			getDividers()

		else:

			# generate file name and hash key
			file_name = "%s_%s" % (selected_file.replace(' ','_'), datetime.datetime.now().strftime("%d-%m-%y"))
			hash_key = "_%s" % hashlib.md5(file_name.encode('utf8')).hexdigest()

			# insert the file name into database with a hash key
			db_engine.execute("INSERT INTO directory (file_name, hash) VALUES ('%s','%s')" % (file_name, hash_key))

			# read file
			if file_ext in ALLOWED_EXT[0:2]:
				df = pd.read_excel('%s/%s' % (DATA_FOLDER_PATH, selected_file))
			else:
				df = pd.read_csv('%s/%s' % (DATA_FOLDER_PATH, selected_file))

			# update the columns names for postgres
			df = df.rename(columns={x:getCorrectColumn(x) for x in df.columns.values})

			# covert dataframe to string
			df = df.astype(str)
			
			# upload the dataframe to database
			df.to_sql(hash_key, db_engine, if_exists="append", index_label='id')

			# show the uploaded message
			print(f"{i} : Data Uploaded : %s" % selected_file)

			getDividers()

