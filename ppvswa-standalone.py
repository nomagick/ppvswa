import bottle
import json

import config
import ppmongo
from ppip import IPPool_LE

def die_of(err):
	res = {'err': True, 'detail': str(err) }
	print(res)
	return json.dumps(res)

def get_json():
	raw = bottle.request.body.read().decode()
	raw = json.loads(raw)
	print(raw)
	return raw

@bottle.route('/signup.ajax')
@bottle.post('/signup.ajax')
def signup():
	try:
		raw = get_json()
	except Exception as e:
		return die_of(e)

	users = ppmongo.VPNUser.load()
	usedip = set(record['ip'] for record in users)
	ippool = IPPool_LE(config.cfgdict['ip-start'] , config.cfgdict['ip-end'] , usedip)
	raw['ip'] = next(ippool)
	
	try:
		newuser = ppmongo.VPNUser(raw)
		newuser.save()
	except Exception as e:
		return die_of(e)
	try:
		ppmongo.SecretFile().deploy(ppmongo.VPNUser.load())
	except Exception as e:
		return die_of(e)
	res = {'err': False}
	return json.dumps(res)

@bottle.route('/signin.ajax')
@bottle.post('/signin.ajax')
def signin():
	try:
		raw = get_json()
	except Exception as e:
		return die_of(e)

	try :
		user = ppmongo.VPNUser.load(_id=raw['_id'],passwd=raw['passwd'])[0]
	except Exception as e:
		die_of(e)
	else:
		res = {'err': False, 'detail': user.argdict}
		return json.dumps(res)

@bottle.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='./static/')

bottle.debug(True)
bottle.run(host='0.0.0.0', port=8080)
