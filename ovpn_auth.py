#! /usr/bin/python3
"""\
==================================================
  OpenVPN username - password auth script 
  Based on mongodb and python3 .
  usage : [set | ask] username password
==================================================\
"""

import sys

import pymongo

cfg = {
	'dbsrv' : 'localhost' ,
	'dbport' : 27017 ,
	'dbuname' : None ,
	'dbpasswd' : None ,
	'dbname' : 'vpn' ,
	'collection' : 'users' ,
	'unamefield' : '_id' ,
	'passwdfield' : 'passwd' ,

	'print_secret' : False ,

}

def query(uname , passwd , write = False):
	res = None
	querydict = {}
	coll = pymongo.collection.Collection(pymongo.database.Database(pymongo.MongoClient(cfg['dbsrv'] , cfg['dbport']) , cfg['dbname']) , cfg['collection'] )
	if not write :
		res = coll.find_one({cfg['unamefield'] : uname , cfg['passwdfield'] : passwd })
		return bool(res)
	else :
		print("Seting password of " + uname + " to " + passwd + " !")
		res = coll.update({cfg['unamefield'] : uname},{'$set' : {cfg['passwdfield'] : passwd }} , True )
		return (not bool(res['err']))

if __name__ == '__main__':
	result = False
	if (len(sys.argv) <= 1) :
		print(__doc__)
		sys.exit(0)
	if sys.argv[1] == 'set' :
		import re
		if re.compile(r'^[a-zA-Z0-9_@\-\.]{0,64}$').match(sys.argv[2]) and re.compile(r'^.{0,64}$').match(sys.argv[3]) :
			result = query(sys.argv[2] , sys.argv[3] , True)
			if result :
				print('Success.')
			else :
				print('Failure!')
		else :
			print('Invalid username or passwd.')
			result = False
	elif sys.argv[1] == 'ask' :
		if query(sys.argv[2] , sys.argv[3]) :
			print ('Valid.')
		else :
			print ('Invalid.')
		result = True
	else :
		try :
			with open(sys.argv[1]) as handle :
				secret = handle.readlines()
				if cfg['print_secret'] :
					print(secret)
				result = query(secret[0].strip(),secret[1].strip())
		except e :
			print(e)

	if result :
		sys.exit(0)
	else :
		sys.exit(1)
