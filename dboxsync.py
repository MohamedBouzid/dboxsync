import dropbox as db
import pymongo 
from pymongo import MongoClient as mongo
import time
from bson.binary import Binary, UUIDLegacy, STANDARD
import sys

# Delete the file that does not exist on the dropbox account from the mongo database 
def removefromdb():
	for doc in filestore.find({}):
		
		if str(doc['name']) not in names:
			filestore.remove({"name" : str(doc['name'])}) 
# Authenticate to dropbox account
try:
	dbx = db.Dropbox(sys.argv[1])
except db.exceptions.ApiError:
	print("connection failure !")	
# Creation of mongodb client
try:
	client = mongo()
except pymongo.errors.OperationFailure:
	print("client creation failure !")
#Creation of a database and collection
db = client.database
filestore = db.files

# Do the job
while 1 :
	names = []

	for entry in dbx.files_list_folder(sys.argv[2]).entries:
		try:		
			meta = dbx.files_alpha_get_metadata(sys.argv[2]+entry.name)	
		except db.exceptions.ApiError:
			print("not found !")		
		names.append(entry.name)
		if (meta.size <= 8*1024**6)  and (entry.name.split('.')[-1] in {"pdf", "docx", "doc", "ppt", "pptx", "jpeg", "jpg", "png"}) :	
			try:			
				m, r = dbx.files_download(sys.argv[2]+entry.name)
			except db.exceptions.ApiError:
				print("download failure !")	
			try:							
				filestore.update({"name" : entry.name}, {"$set" : {"name" : entry.name, "file" : Binary(r.content), "meta" : str(m)}}, upsert=True )
			except pymongo.errors.OperationFailure:
				print("Update failed !")
	print(filestore.count())

	removefromdb()
	
	#time.sleep( 1 )

