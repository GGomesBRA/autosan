from pyautocad import Autocad, APoint
from operator import itemgetter

from objectEngine import getObjectbyID

class knot():
	coordinate = 0
	ztampa = 0
	profundidade = 0

def getPointInfo():

	acad = Autocad()
	acad.prompt("Hello, Autocad from Python\n")

	print(acad.doc.Name)

	count=0
	pointarray=[]

	pointID = {}

	for obj in acad.iter_objects():

		if obj.EntityName == 'AcDbPoint' :

			print(type(obj))
			print(obj.Coordinates)
			coord = obj.Coordinates
			print(obj.ObjectID)
			ID = obj.ObjectID
			print(obj.ObjectName)
			print(obj.EntityName)
			print(obj.EntityType)

			pointC = APoint(obj.Coordinates[0], obj.Coordinates[1])
			p1 = APoint(obj.Coordinates[0]+0.5, obj.Coordinates[1]-0.5)

			text = acad.model.AddText('Point %s' % count, p1, 1.0)
			
			pointarray.append(pointC)

			point=knot()
			point.coordinate = coord

			pointID[count]={"id":ID,"inst":point}
			
			count+=1

		else:
			print('Não é ponto é:'+str(obj.EntityType))
			print('Não é ponto é:'+str(obj.EntityName))

	print(pointID)

def getSrtLst(adutoras):

	acad = Autocad()
	count=0

	pointID = {}

	countcurvas=0
	counttubo=0
	pointarray=[]

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

def buildPoints():
	acad=Autocad()

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

	# print("curvas   "+str(curvas))
	print("adutoras   "+str(adutoras))

	for ele in adutoras:

		pointsArray=[]

		# print(adutoras[ele]["id"])
		identity=adutoras[ele]["id"]

		obj1 = getObjectbyID(identity)
		# print(obj1.Coordinates)

		for cn in curvas:

			# print(curvas[cn]["id"])
			identity=curvas[cn]["id"]

			cnobj = getObjectbyID(identity)

			# print("CN NUMBER")
			# print(cnobj)

			cnobj.Elevation = 0.00
			interpoint = obj1.IntersectWith(cnobj, 0)
			# print(interpoint)

			if len(interpoint) == 0:
				pass
				# print("Sem intersect")
			else:
				i = int(len(interpoint)/3)
				for c in range(i):
					point = APoint(interpoint[3*c],interpoint[3*c+1],curvas[cn]["elev"]*1.1)
					acad.model.AddPoint(point)
					pointsArray.append(interpoint[3*c])
					pointsArray.append(interpoint[3*c+1])
					pointsArray.append(curvas[cn]["elev"]*1.1)

			cnobj.Elevation = curvas[cn]["elev"]

		points=tuple(pointsArray)
		# print(points)
	return {"Adutoras":adutoras,"Curvas":curvas}