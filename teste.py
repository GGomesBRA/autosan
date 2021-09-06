from pyautocad import Autocad, APoint
from pointEngine import knot
import itertools
from testscript import getObjectbyID

from operator import itemgetter

acad = Autocad()
p1 = APoint(0, 0)

print(acad)
print(p1)

for obj in acad.iter_objects():
	if obj.EntityName == 'AcDbPoint' :
		pass
		# print(type(obj))
		# print(obj.Coordinates)
		# coord = obj.Coordinates
		# print(obj.ObjectID)
		# ID = obj.ObjectID
		# print(obj.ObjectName)
		# print(obj.EntityName)
		# print(obj.EntityType)


count=0

pointID = {}

countcurvas=0
counttubo=0
pointarray=[]

curvas = {}
adutoras = {}

for obj in acad.iter_objects():

	if obj.EntityName == 'AcDbPolyline' and (obj.Layer == 'CN_PRINCIPAL' or obj.Layer == 'CN_INTERMED'):

		ID = obj.ObjectID

		curvas[countcurvas]={"id":ID, "elev":obj.Elevation}
		
		countcurvas+=1

	elif obj.EntityName == 'AcDbPolyline' and obj.Layer == 'ADUTORA':

		ID = obj.ObjectID

		adutoras[counttubo]={"id":ID}
		
		counttubo+=1

startp=[]

for adutora in adutoras:
	print(adutora)
	tubestart=getObjectbyID(adutoras[adutora]["id"])
	print(tubestart.Coordinates[0:2])
	for i in range(2):
		startp.append(tubestart.Coordinates[i])
	startp.append(tubestart.Elevation)
	print(startp)

ptlst = []

for obj in acad.iter_objects():

	if obj.EntityName == 'AcDbPoint' :

		# print(type(obj))
		# print(obj.Coordinates)
		# print(obj.ObjectName)
		# print(obj.EntityName)
		# print(obj.EntityType)
		# print(obj.ObjectID)
		
		ID = obj.ObjectID
		coord = obj.Coordinates

		pointC = APoint(obj.Coordinates[0], obj.Coordinates[1])
		p1 = APoint(obj.Coordinates[0]+0.5, obj.Coordinates[1]-0.5)
		distance = pointC.distance_to(startp)

		print(distance)

		ptlst.append([distance,ID])

		text = acad.model.AddText('Point %s' % distance, p1, 1.0)
		
		count+=1

		pointarray.append(pointC)

		pointID[count]={"id":ID,"coord":coord,"inst":knot()}
		knot

	else:
		print('Não é ponto é:'+str(obj.EntityType))
		print('Não é ponto é:'+str(obj.EntityName))

srtedlst = sorted(ptlst, key=itemgetter(0))
print(srtedlst)

