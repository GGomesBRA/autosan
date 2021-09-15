import os
from comtypes import COMError
from comtypes.client import CreateObject, GetActiveObject


def main():
	try: 
		#Get AutoCAD running instance
		acad = GetActiveObject("AutoCAD.Application")
		state = True
	except(OSError,COMError): 
		#If autocad isn't running, open it
		#I never tried to go through this exception, i prefer to always run autocad and then run my script
		print("Exception on cad getting")
		acad = CreateObject("AutoCAD.Application",dynamic=True)
		state = False
    
    #instantiate a doc object with the active document of autocad. You could also choose by name
    #we print the name in console just to be sure.
    #my document is named "drawing2.dwg" yours should be the name of the .dwg file you opened
	
	doc=acad.ActiveDocument
	print(doc.name)

	#ok, so now we need to plot our component, plotting will automatically save our drawing as .pdf file inside some folder
	#i have a layout tab to the right of my model tab, i will use it to configure my plotting and do the task i need

	# i get the layouts within my doc object
	# generally speaking you will have a model tab and a layout1 tab. usually the layout1 tab is renamed, but i will just use my layout1 tab, i will make the console print out wvery layout inside layouts object, just for informational purposes
	layouts = doc.Layouts
	print(layouts.count)

	for i in range(layouts.count):
		print(layouts.Item(i).name)

	#I will get my layouty object by selecting an Item from layouts obj, this time i will select it by name, just to show you it is possible.
	my_layout = layouts.Item("Layout1")
	print(my_layout.name)

	#i will get the plot object within our document now
	# we need the plot obj to actually send the command to plot to a file
	plotobj = doc.Plot
	print(plotobj)
	#set the layouts to plot to our layout1

	#now we can use the method "PlotToFile"
	#i selected the dwg to pdf pc3 file
	#you could select any pc3, by its name
	my_plot_job = plotobj.PlotToFile("my_plotname","DWG To PDF.pc3")
	print(my_plot_job)

	# after this, the job is started and you can check that your printer symbol on the bottom right corner of your autocad will show a printing animation.
	# after the job is done (it should take like 30sec) you can check your page in your windows documents folder

main()
