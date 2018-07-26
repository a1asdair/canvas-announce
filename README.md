# canvas-announce
This is a simple routine to support the editing and scheduling of announcements in Canvas. This is an alpha release that is still going through testing, so please do report any bugs that you experience.

## Quick Start
* Export the Canvas course that includes the announcements you want to edit/schedule
* Run canvas-announce.exe in the same directory as the course export. This will create a CSV file called announcements.csv
* Edit the CSV. You can change the title, message and delay fields.
* Use the 'Include' field to indicate which announcements should be imported ('1') and excluded ('0')
* Save the CSV file leaving the filename unchanged i.e. ```announcements.csv```
* Run canvas-announce.exe again. This will create a Canvas course packagae for import.
* Import the course package into your new Canvas module, and select only the Announcements for import
* Check that the announcements listed, and their schedule, match your ```announcements.csv``` file.  

## File descriptions  
* *canvas-announce.py* is the Python source code for the program. You can donwload and run this in your own Python environment.  
* *canvas-announce.exe* is a standalone executable file for Windows PC, compiled using PyInstaller, that can be downloaded and run without needing a Python installation.  

## What is the program doing?
This program parses and edits a course export package from Canvas to allow you to more easily edit and schedule course announcements. It requires a course export in .imscc format. It identifies announcements within that package, and summarises them in a CSV file for editing. Once you have edited the announcements, it then re-packages them back into an .imscc file for re-importing to Canvas. It only edits the announcement files, and all other files in the course package are retained unedited.  

When you run the program there must be only one .imscc file in the folder.  If more than one is present (e.g. an import file from a previous run) the program will quit with an error as it is ambigous which file is to be used for the extract.  

The program leaves the original course package unedited, and saves a new one with the prefix 'IMPORT_'. It also renames the edited announcements.csv to append the date and time to avoid accidental overwrites.  If you want to re-use a previous announcements.csv file, just rename it to its original ```announcements.csv``` filename. The program does create some temporary files while running, but these are deleted again on completion.  

## Exporting a Course from Canvas before you begin
You need to export your course content as an .imscc file before you start.  You can find instructions on how to do that [here](https://community.canvaslms.com/docs/DOC-12785-415241323). Save this export in a folder together with the canvas-announce.exe.  

## Importing a Course to Canvas again after you have edited the announcements
Importing the edited course package is similar to exporting.  The difference is that you only import selected content i.e. just the announcements. Of course, as the rest of the course package is unchanged, if you know you want to import other elements alongside the announcements that's ok (but make sure you know what you are doing).  You can find instructions on importing course pacakages [here](https://community.canvaslms.com/docs/DOC-10713-67952724501), but make sure you [import selected content](https://community.canvaslms.com/docs/DOC-13101-4152497985) when you do the import or else you will re-import the whole course. 

## Limitations
The program does not currently allow you to create new course packages, or to add announcements to a course package.  It only allows the editing (or removal) of existing announcements that you have exported from a course. The course package import still contains all the material, so for a large course the import processing can be slow as Canvas processes the whole file before allowing you to select just the announcements for import.

## Guidance for editing the Announcements
### Announcement Titles
These should be entered in plain text.  
Example:  
```First Teaching Day this Saturday```
### Announcement text
These should be entered using html tags.  This allows links and some basic formatting of messages.  
Example:  
```html
<p>Just a quick reminder about the upcoming Day 3 this Saturday 4th November.</p>
<p>We will begin at 10:15am as usual in 2Y5.</p>
```
### Delay dates
These need to be entered in the format YYYY-MM-DDTHH:MM:SS
Note that years are four digits, months and days are two digits (i.e. include leading zeroes) and the time is in the 24 clock (include leading zeroes). Note also the character 'T' separating the date and the time.  
Examples:  
```2018-11-29T15:00:00```  
```2018-12-10T10:00:00```
