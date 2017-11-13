class GenList(object):

	def __init__(self):
		self.vector = []

	def __len__(self):
		return len(self.vector)
	
	def getObjVal(self, obj):
		
		if isinstance(obj, str):
			return obj
		elif hasattr(obj, "getName"):
			return obj.getName()
		else:
			return None

	def get(self, obj):
		objVal = self.getObjVal(obj)
		if objVal == None:
			return None

		_objs = filter(lambda el: el.getName() == objVal, self.vector)

		if len(_objs) > 0:
			return _objs[0]
		else:
			return None

	def getAll(self):
		return self.vector

	def getAllSortedByKey(self, keyFunction):
		return sorted(self.vector, key = keyFunction)

	def add(self, obj):
		_obj = self.get(obj)
		if _obj == None:
			self.vector.append(obj)

	def addAll(self, objList):
		if objList != None:
			for obj in objList:
				_obj = self.get(obj)
				if _obj == None:
					self.vector.append(obj)

	def remove(self, obj):
		_obj = self.get(obj)

		if _obj != None:
			self.vector.remove(_obj)

	def has(self, obj):
		_obj = self.get(obj)

		return _obj != None
