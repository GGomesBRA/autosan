import os
import comtypes.client
from comtypes import COMError
from comtypes.client import CreateObject, GetActiveObject
import math
import time

from pyautocad import Autocad, APoint
import win32com.client

import itertools

from pointEngine import getPointInfo, knot, getSrtLst, buildPoints
from objectEngine import getObjectbyID

# DO NOT FORGET HOW TO SOLVE THE ISSUE WITH INVALID CLASS TYPES >>>>>>

# A colleague and I were diagnosing this exact issue. I couldn't believe how obscure this was and we found the solution 
# by searching similar issues with .NET equivalent code:

# To fix, create a folder called 'Desktop' in:

# 'C:\Windows\SysWOW64\config\systemprofile\' on 64bit
# 'C:\Windows\System32\config\systemprofile\' on 32bit

# This genuinely fixed an absolutely identical issue.


def getTubeExt(line):
	start = line.StartPoint
	end = line.EndPoint

	distance = math.sqrt((end[0]-start[0])*(end[0]-start[0])+(end[1]-start[1])*(end[1]-start[1]))

	return distance

def writeInfotoLine(line,count):
	acad = Autocad()
	start = line.StartPoint
	end = line.EndPoint

	angle = math.atan((end[1]-start[1])/(end[0]-start[0]))

	ext = str(round(getTubeExt(line),2))

	mx = start[0]+((end[0]-start[0])/2)
	my = start[1]+((end[1]-start[1])/2)
	mpoint = APoint(mx, my)

	texttoadd = acad.model.AddText('Extensão: %s' % ext, mpoint, 0.2)
	texttoadd.Rotation = angle
	texttoadd.Alignment = 1
	texttoadd.TextAlignmentPoint = mpoint



	texttoadd = acad.model.AddText('Trecho: %s' % str(count), mpoint, 0.2)
	texttoadd.Rotation = angle
	texttoadd.Alignment = 7
	texttoadd.TextAlignmentPoint = mpoint

	return angle

def checkLines():
	acad = Autocad()
	count = 0
	for obj in acad.iter_objects():
		if obj.EntityName == 'AcDbLine' :
			writeInfotoLine(obj,count)
			count+=1




def go():


	acad1 = win32com.client.Dispatch("AutoCAD.Application")


	acad = Autocad()
	acad.prompt("Hello, Autocad from Python\n")
	#raise
	print(acad.doc.Name)

	# p1 = APoint(0, 0)
	# p2 = APoint(50, 25)
	# for i in range(5):
	#     text = acad.model.AddText('Hi %s!' % i, p1, 2.5)
	#     acad.model.AddLine(p1, p2)
	#     acad.model.AddCircle(p1, 10)
	#     p1.y += 10

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
			
			count+=1

			pointarray.append(pointC)

			pointID[count]={"id":ID,"coord":coord,"inst":knot()}
			knot

		else:
			print('Não é ponto é:'+str(obj.EntityType))
			print('Não é ponto é:'+str(obj.EntityName))

	itera = itertools.combinations(pointarray,2)
	for ele in itera:
		acad.model.AddLine(ele[0],ele[1])
	# for point in pointarray:
	# 	start = point
	# 	for end in pointarray:
	# 		if end != start:
	# 			line = acad.model.AddLine(start,end)
	    
	# dp = APoint(10, 0)
	# for text in acad.iter_objects('Text'):
	#     print('text: %s at: %s' % (text.TextString, text.InsertionPoint))
	#     text.InsertionPoint = APoint(text.InsertionPoint) + dp

	# for obj in acad.iter_objects():
	#     # print(dir(obj))
	# 	try:
	# 		obj.Explode
	# 		print(obj.EntityName)
	# 		print(obj.EntityType)
	# 		print(obj.ObjectName)
	# 		print(obj._IAcadBlockReference__com__get__Name)
	# 		print('objeto explodido')
	# 		print('')
	# 	except:
	# 		print(obj.EntityName)
	# 		print(obj.EntityType)
	# 		print(obj.ObjectName)
	# 		print('Objeto nao explodido')
	# 		print('')



	# # iterate through all objects (entities) in the currently opened drawing
	# # and if its a BlockReference, display its attributes.
	# for entity in acad.ActiveDocument.ModelSpace:
	#     name = entity.EntityName
	#     print(name)
	#     if name == 'AcDbBlockReference':
	#         print('ENTROU')
	#         HasAttributes = entity.HasAttributes
	#         print(HasAttributes)
	#         if HasAttributes:
	#             for attrib in entity.GetAttributes():
	#                 print("  {}: {}".format(attrib.TagString, attrib.TextString))
	#         print(dir(entity))
	#         print(entity.__getattr__)
	#         entity.Explode()

	#     if name == 'AcDbPoint':
	#         print('ENTROU')

	#         getxdata = entity.GetXData

	#         print(getxdata)

	#         Coordinate = entity.Coordinate
	#         Coordinates = entity.Coordinates



	#         print(Coordinate)
	#         print(Coordinates)
	#         if HasAttributes:
	#             for attrib in entity.GetAttributes():
	#                 print(attrib)
	#         print("Passou")
	#         print(dir(entity))
	#         print(entity.__getattr__)
	#         entity.Explode()

	# c1=[0.00,0.00,0.00]
	# c2=[500.00,500.00,500.00]



	# p1 = APoint(15, 15)
	# p2 = APoint(30, 30)
	# p3 = APoint(45, 15)

	# print(p2)

	# print(type(acad.model))


	# acad1.ActiveDocument.ModelSpace.AddLine(p1, p2)
	# acad1.ActiveDocument.ModelSpace.AddLine(p2, p3)



def calculate(x,r):
	xlinha = x*math.pi/(r*90)
	# y = r*x*(1-x)
	y = 200*(math.sin(xlinha))

	return y

def main():
	try: #Get AutoCAD running instance
		acad = GetActiveObject("AutoCAD.Application")
		state = True
	except(OSError,COMError): #If autocad isn't running, open it
		print("Exception on cad getting")
		acad = CreateObject("AutoCAD.Application",dynamic=True)
		state = False
    
	doc=acad.ActiveDocument
	activestate = doc.Blocks.Count

	print(activestate)

	for r in range(3):
		if r == 0:
			pass
		# strtouse=input('enter amplitude multiplier:')
		# r=int(strtouse)
		else:
			command='line '
			for x in range(200):
				point = str(x)+','+str(calculate(x,r))+' '
				command += point

			command += '\n'
			# print(command)

		    #Our example command is to draw a line from (0,0) to (5,5)
			command_str = 'line 0,0 50,50 75,75 \n' #Notice that the last SPACE is equivalent to hiting ENTER
		    #You should separate the command's arguments also with SPACE
			commanda = 'select '

			#Send the command to the drawing
			doc.SendCommand(command)

		time.sleep(1)



def make3DPoly(array):

	npoints = int(len(array)/3)

	for c in range(npoints):
		pointstart = APoint(interpoint[3*c],interpoint[3*c+1],curvas[cn]["elev"]*1.1)
		pointend = APoint(interpoint[3*c+3],interpoint[3*c+1+3],curvas[cn]["elev"]*1.1)
		acad.model.AddPoint(point)
		pointsArray.append(interpoint[3*c])
		pointsArray.append(interpoint[3*c+1])
		pointsArray.append(curvas[cn]["elev"]*1.1)


def getCNdata():

	acad = Autocad()
	acad.prompt("Hello, Autocad from Python\n")

	# print(acad.doc.Name)
	objdict = buildPoints()

	getSrtLst(objdict["Adutoras"])






class Tubo():
	alltubes=[]

	def __init__(self, extensão, trecho, ki, zi, kz, zf, ):
		self.__class__.instances.append(self)

		self.name = trecho
		
		self.r = 0
		self.i = 0

	@classmethod
	def printTubes(cls):
		for tube in cls.alltubes:
			print(tube)


class AreaContrib():

	def __init__(self, contrib):
		contrib = 0


#Execution Part
if __name__ == '__main__':
    # main()
    getCNdata()
