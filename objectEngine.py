from pyautocad import Autocad, APoint

def getObjectbyID(identity):

	acad = Autocad()

	for obj in acad.iter_objects():

		if obj.ObjectID == identity:
			acadObj = obj
			return acadObj