'''
2012-8-3
@avastms
ipv4 arranger
'''
class IPPool (object):
	"""docstring for IPPool """
	def __init__(self, Start , End):
		if not (self.isvalid(Start) and self.isvalid(End)) :
			raise ValueError
		self.start = [int(x) for x in min(Start , End).split ('.')]
		self.end = [int(x) for x in max(Start, End ).split ('.')]
		self.used = set({})
		self.iterlist = [None,None,None,None]
		self.cache = None
		self.EOF = False
		for x in range(0,4) :
			self.iterlist[x] = iter( range (  self.start[x] ,self.end[x] +1 ) )
		if not ( self.start[0] == self.end[0] and self.start[1] == self.end[1] and self.start[2] == self.end[2] ) :
			self.iterlist[3] = iter ( range ( self.start[3] , 255 ) )
			self.iterlist.append (iter ( range ( 1 , self.end[3] +1 ) ) )
		self.__iter__()
		self.__next__()
	def __iter__ (self) :
		self.cache = self.start if self.cache == None else self.cache
		return self
	def __str__ (self) :
		return str(self.cache[0]) + '.' + str(self.cache[1]) + '.' + str(self.cache[2]) + '.' + str(self.cache[3])
	def __next__ (self) :
		register = str(self)
		for x in reversed (range(0,4)) :
			try :
				self.cache[x] = next(self.iterlist[x])
			except StopIteration :
				continue
			else :
				if x != 3 :
					for y in range (x+1 , 4) :
						self.iterlist[y] = iter ( range ( 1 , 255 ) )
						self.cache[y] = next(self.iterlist[y])
					if len(self.iterlist) == 5 and self.isedge()  :
						self.iterlist[3] = self.iterlist.pop()
						self.cache[3] = next (self.iterlist[3])
				if self.isused (register) :
					return next(self)
				else :
					return register
		if self.EOF == False :
			self.EOF = True
			return self.spit(register)
		else :
			raise StopIteration
	def isvalid (self , IPString) :
		i=0
		for x in IPString.split('.') :
			i += 1
			if not 255 > int(x) >= 0 :
				return False
			if i == 4 and x == 0 :
				return False
		return True
	def isused (self , IPString = None) :
		if IPString :
			return True if ( IPString in self.used )else False
		else :
			return True if (str(self) in self.used )else False
	def isedge (self , IPString = None , Stage = 3) :
		if IPString :
			target = [int(x) for x in IPString.split('.')]
		else :
			target = self.cache
		for x in range (0,Stage) :
			if self.end[x] != target[x] :
				return False
		return True

	def spit (self , IPString = None) :
		if IPString :
			x = IPString
		else :
			x = None
		if self.isused(x) :
			return next(self)
		else :
			return IPString if x else str(self)
	def occupy (self , IPString) :
		return self.used.add(IPString)
	

def IPPool_LE (Start , End , Used = {}) :
	startlist , endlist = [int(x) for x in Start.split('.')] , [int(x) for x in End.split('.')]
	while True :
		startlist[3] += 1
		for x in  reversed (range (0,4)) :
			if startlist[x] >= 255 :
				startlist[x] = 1
				try :
					startlist[x-1] += 1
				except IndexError :
					raise StopIteration
					break
		cache = str(startlist[0]) + '.' + str(startlist[1]) + '.' + str(startlist[2]) + '.' + str(startlist[3])
		if startlist < endlist :
			if cache in Used :
				continue
			else :
				yield cache
		else :
			raise StopIteration 
