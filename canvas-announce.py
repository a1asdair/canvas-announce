# ----------------------------------------------
#
# canvas-announce.py
# A package for editing and scheduling Announcements in
# Canvas courses/modules.
# Professor Alasdair Rutherford
# University of Stirling
# (c) 2018 
# Documentation available at https://github.com/a1asdair/canvas-announce

# Created:		25th July 2018
# Last edited:	26th July 2018 


import time
from time import sleep
import csv
import os
import zipfile
from os import listdir
from os.path import isfile, join
import shutil
import xml.etree.ElementTree
from shutil import copyfile

outputpath = './'


def getzipfile(zippath):

	zf = zipfile.ZipFile(zippath, mode='r')
	#print('| ', zf.infolist())
	filelist = []
	metalist = []
	counter = 0
	for item in zf.namelist():
		if item.find('/')<0 and item.endswith('.xml'): # and len(item)>20:
			filelist.append(item)
			counter+=1
		else:
			metalist.append(item)
	#zf.close
	print('| Found', counter, 'files.')

	return filelist, metalist, zf


def findannouncements(zipf, filelist, outputpath):

	anndict = {}
	counter = 0

	for file in filelist:

		with zipf.open(file) as xmlfile:

			#print(xmlfile)
			e = xml.etree.ElementTree.parse(xmlfile).getroot()
			xtype=''
			topicid=''
			position=''
			delay=''
			title=''
			state=''
			for child in e:
				#print(child.tag, '			', child.attrib)
				if child.tag == '{http://canvas.instructure.com/xsd/cccv1p0}type':
					xtype = child.text		
				if child.tag == '{http://canvas.instructure.com/xsd/cccv1p0}topic_id':
					topicid = child.text
				if child.tag == '{http://canvas.instructure.com/xsd/cccv1p0}position':
					position = child.text
				if child.tag == '{http://canvas.instructure.com/xsd/cccv1p0}title':
					title = child.text
				if child.tag == '{http://canvas.instructure.com/xsd/cccv1p0}delayed_post_at':
					delay = child.text
				if child.tag == '{http://canvas.instructure.com/xsd/cccv1p0}workflow_state':
					state = child.text				
			if xtype=='announcement':
				#print(file, '|', topicid, '|', position, '|', state)
				with zipf.open(topicid + '.xml') as contentfile:
					ec = xml.etree.ElementTree.parse(contentfile).getroot()
					for child in ec:
						if child.tag == '{http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1}text':
							contenttext = child.text		
				anndict[file]={'id': file, 'topicid': topicid, 'title': title, 'message': contenttext, 'delay': delay, 'include': '1'}
				counter+=1
	print('| Processed', counter, 'announcements.')

	with open(outputpath + 'announcements.csv', 'w', newline='') as announcements_file:
		fieldnames = ['id', 'topicid', 'title', 'message', 'delay', 'include']
		writer = csv.DictWriter(announcements_file, fieldnames = fieldnames)
		writer.writeheader()
		for row in anndict:
			writer.writerow(anndict[row])
	print('| Announcements extracted and saved in')
	print('|' + outputpath + 'announcements.csv ready for editing.')


def outputeditedannouncements(zf, filelist, outputpath):

	try:
		os.mkdir(outputpath + 'temp')
		print('| Temp folder created')
	except:
		print('| Temp folder already exists')

	print('| ')
	print('| Processing Announcements (* = Included, X = Excluded)')

	anncounter = 0
	inccounter = 0

	with open(outputpath + 'announcements.csv', 'r', newline='') as announcements_file:
		reader = csv.DictReader(announcements_file)
		sortedlist = sorted(reader, key=lambda row: row['delay'], reverse=False)
		print('| ', end='')
		positioncount = 1

		for row in sortedlist:
			filelist.remove(row['id'])
			anncounter +=1
			if row['include']=='1':

				filelist.remove(row['topicid'] + '.xml')
				inccounter +=1

				# Edit meta-data file
				print(' *', end='')
				xmlfile = zf.open(row['id'])
				ET = xml.etree.ElementTree
				ET.register_namespace('', "http://canvas.instructure.com/xsd/cccv1p0")	
				tree = ET.parse(xmlfile)
				e = tree.getroot()		
				#print(e['{http://canvas.instructure.com/xsd/cccv1p0}position'].text)
	
				pos = e.find('{http://canvas.instructure.com/xsd/cccv1p0}position')
				if pos is None:
					e.append(ET.Element('{http://canvas.instructure.com/xsd/cccv1p0}position'))
				pos = e.find('{http://canvas.instructure.com/xsd/cccv1p0}position')
				pos.text = str(positioncount)
				positioncount+=1
	
				delay = e.find('{http://canvas.instructure.com/xsd/cccv1p0}delayed_post_at')
				if delay is None:
					e.append(ET.Element('{http://canvas.instructure.com/xsd/cccv1p0}delayed_post_at'))
				delay = e.find('{http://canvas.instructure.com/xsd/cccv1p0}delayed_post_at')
				delay.text = row['delay']

				title = e.find('{http://canvas.instructure.com/xsd/cccv1p0}title')
				if title is None:
					e.append(ET.Element('{http://canvas.instructure.com/xsd/cccv1p0}title'))
				title = e.find('{http://canvas.instructure.com/xsd/cccv1p0}title')
				title.text = row['title']
	
				state = e.find('{http://canvas.instructure.com/xsd/cccv1p0}workflow_state')
				if state is None:
					e.append(tree.Element('{http://canvas.instructure.com/xsd/cccv1p0}workflow_state'))
				state = e.find('{http://canvas.instructure.com/xsd/cccv1p0}workflow_state')
				state.text = 'post_delayed'	

				tree.write(outputpath + 'temp/' + row['id'], encoding='UTF-8')

				# Edit Content file
				contentfile = zf.open(row['topicid'] + '.xml')
				ET = xml.etree.ElementTree
				ET.register_namespace('', "http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1")	
				tree = ET.parse(contentfile)
				e = tree.getroot()		
				#print(e['{http://canvas.instructure.com/xsd/cccv1p0}position'].text)
	
				t = e.find('{http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1}text')
				if t is None:
					e.append(ET.Element('{http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1}text'))
				t = e.find('{http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1}text')
				t.text = row['message']

				title = e.find('{http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1}title')
				if title is None:
					e.append(ET.Element('{http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1}title'))
				title = e.find('{http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1}title')
				title.text = row['title']

				tree.write(outputpath + 'temp/' + row['topicid'] + '.xml', encoding='UTF-8')
			else:
				print(' X', end='')
		print(' |')

		print('| ')
		print('| Processing other files in ZIP (* = Included, X = Excluded)')
		print('| ', end='')

		othercounter = 0

		for remaining in filelist:
			othercounter +=1
			xmlfile = zf.open(remaining)
			#ET = xml.etree.ElementTree
			#ET.register_namespace('', "http://canvas.instructure.com/xsd/cccv1p0")		
			#tree = ET.parse(xmlfile)
			#tree.write(outputpath + 'temp/' + remaining, encoding='UTF-8')
			uneditedfile = open(outputpath + 'temp/' + remaining, "wb")
			uneditedfile.write(xmlfile.read())
			uneditedfile.close()
			print(' *', end='')
		print(' |')
		print('| ')
		print('| Processed', anncounter, 'announcements, and included', inccounter, 'of them.')
		print('| Included an additional', othercounter, 'files in the ZIP.')
		print('| ')


def saveeditedzipfile(zin, editedfilelist, metalist, outputpath, zipname):

	#print(filelist)

	with zipfile.ZipFile(outputpath + 'IMPORT_' + zipname, 'w') as zout:
			for item in editedfilelist:
				editedfile = open(outputpath + 'temp/' + item, "rb")
				zout.writestr(item, editedfile.read())
				editedfile.close()
			for item in metalist:
				zout.writestr(item, zin.read(item))
	print('| ZIP file saved to', outputpath + 'IMPORT_' + zipname)
	print('| ready to be imported into Canvas.')



def findzipfile(outputpath):

	print('| Checking for Canvas packages ...')

	onlyfiles = [f for f in listdir(outputpath) if isfile(join(outputpath, f))]
	zipfiles = []
	for file in onlyfiles:
		if file.endswith('.imscc'):
			zipfiles.append(file)
	if len(zipfiles)==1:
		print('| Found a Canvas package at ', outputpath + zipfiles[0])
		return outputpath + zipfiles[0], zipfiles[0]
	else:
		print('*** ERROR: NO UNIQUE CANVAS MODULE PACKAGE FOUND ***')
		print(' Please make sure there is only one Canvas export in the folder.')
		exit()


def printheader():

	print(' __________________________________________________________')
	print('| ')
	print('| Program to extract and edit Canvas Module Announcements')
	print('| By Alasdair Rutherford, 2018')
	print('|_________________________________________________________')
	print('')
	#print('')


# Main Program

if os.path.isfile(outputpath + 'announcements.csv'):

	# This triggers on the second running, when an announcements.csv
	# file has been created and edited.

	printheader()

	zippath, zipname = findzipfile(outputpath)

	print('| Process the ZIP for import')

	filelist, metalist, zf = getzipfile(zippath)

	# After editing by user, update the XML files
	outputeditedannouncements(zf, filelist,outputpath)

	# Insert the edited files into the Content Package for re-importing
	onlyfiles = [f for f in listdir(outputpath + 'temp/') if isfile(join(outputpath + 'temp/', f))]
	saveeditedzipfile(zf, onlyfiles, metalist, outputpath, zipname)

	# Back-up edited announcement file
	os.rename(outputpath + 'announcements.csv', outputpath + 'announcements-edit-' + str(time.gmtime().tm_hour) + '-' + str(time.gmtime().tm_min) + '_' + str(time.gmtime().tm_mday) + '-' + str(time.gmtime().tm_mon) + '-' + str(time.gmtime().tm_year)+ '.csv')

	# Tidy up
	sleep(4)
	try:
	    shutil.rmtree(outputpath + 'temp/')
	except OSError as e:
	    print ("Error: %s - %s." % (e.filename, e.strerror))
	
	zf.close

	print('| Done')
	print('|____________________________________________')

else:

	# This triggers on the first run, to extract Announcements
	# and create the announcements.csv file.

	printheader()

	zippath, zipname = findzipfile(outputpath)

	print('| Extract the announcements for editing')

	# Get the details fron the Content Package
	filelist, metalist, zf = getzipfile(zippath)

	# Identify the announcements from the files in the root
	findannouncements(zf, filelist, outputpath)

	zf.close

	print('| ')
	print('| Done')
	print('|____________________________________________')


input("Press Enter to exit the program ...")