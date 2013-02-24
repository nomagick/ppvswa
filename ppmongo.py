import pymongo
import re

import config

class VPNUser(object):
	"""class for VPNUser"""
	schema = dict((x,re.compile(y)) for (x,y) in [
		('_id', r"^[\S]{1,20}@[\S]{1,20}\.[\S]{1,10}$"),	#emal as username , primary key
		('srv' , r"^[\S]*$"),								#server name
		('passwd' , r"^[\S]{1,64}$"),						#password
		('ip' , r"^(((\d{1,3}\.){3}\d{1,3})|\*)$"),			#assigned ipv4 address
		('status' , r"^[01]{1}$"),							#active status
		('message' ,r"^.{0,4096}$"),						#other information
		])
	resources = {
		'dbconn' : None	,	#connection object of mongodb
		'db' : None,		#db object of mongodb
		'dbcoll' : None		#user collection of mongodb
	}

	def __init__(self, argdict):
		super(VPNUser, self).__init__()
		self.argdict = argdict
	def __getitem__(self,key):
		try:
			return self.argdict[key]
		except KeyError :
			return config.defdict[key]
	def __setitem__(self,key,value):
		self.argdict[key] = value
	def __delitem__(self,key):
		del(self.argdict[key])

	@staticmethod
	def init_db(config = config.cfgdict):		#<----information provided by config.py
		VPNUser.resources['dbconn'] = pymongo.MongoClient(config['dbserver'] , config['dbport'])
		VPNUser.resources['db'] = pymongo.database.Database(VPNUser.resources['dbconn'] , config['dbname'])
		if config['dbuser'] and config['dbpasswd'] :
			VPNUser.resources['db'].authenticate(config['dbuser'],config['dbpasswd'])
		VPNUser.resources['dbcoll'] = pymongo.collection.Collection(VPNUser.resources['db'] , 'vpnuser')

	def save(self, force = False):
		if not VPNUser.resources['dbcoll'] :
			VPNUser.init_db()
		querydict=dict(
			(x,self[x]) for x in VPNUser.schema if VPNUser.schema[x].match(self[x])
			)
		if querydict.keys() != VPNUser.schema.keys() : 
			raise ValueError('pattern dismatch')
		print(querydict)
		if force:
			VPNUser.resources['dbcoll'].update({'_id': querydict['_id']} ,querydict , True , False )
		else:
			VPNUser.resources['dbcoll'].insert(querydict)

	def update(self,**argdict):
		if '_id' in argdict :
			raise ValueError('illegal attempt to update _id.')
		self.argdict.update(argdict)
		self.save(force=True)

	def remove(self):
		VPNUser.resources['dbcoll'].remove({'_id': querydict['_id']})

	@staticmethod
	def load(**argdict):
		if not VPNUser.resources['dbcoll'] :
			VPNUser.init_db()
		return [VPNUser(x) for x in VPNUser.resources['dbcoll'].find(argdict)]

	def __str__(self):
		return self['_id'] + '\t' + self['srv'] + '\t' + self['passwd'] + '\t' + self['ip'] + '\n'

class SecretFile(object):
	"""docstring for SecretFile"""
	def __init__(self, path=config.cfgdict['secret-path']):
		super(SecretFile, self).__init__()
		self.targetfile = path + 'chap-secrets'
		self.oldfile = path + 'chap-secrets.old'

	def deploy(self, records):
		tmpstr=''
		with open(self.targetfile , 'w') as t_handle:
	 		for item in records :
	 			if item['status'] == '1':
	 				tmpstr += str(item)
	 		try:
	 			with open(self.oldfile) as o_handle:
	 				tmpstr += o_handle.read()
	 		except:
	 			pass
	 		finally:
	 			t_handle.write(tmpstr)
	 			
