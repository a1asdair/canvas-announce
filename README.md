# canvas-announce
This is a simple routine to support the editing and scheduling of announcements in Canvas. This is an alpha release that is still going through testing, so please do report any bugs that you experience.

## Quick Start
* Export the Canvas course that includes the announcements you want to edit/schedule
* Run canvas-announce.exe in the same directory as the course export. This will create a CSV file called announcements.csv
* Edit the CSV. You can change the title, message and delay fields.
* Use the 'Include' field to indicate which announcements should be imported ('1') and excluded ('0')
* Save the CSV file
* Run canvas-announce.exe again. This will create a Canvas course packagae for import.
* Import the course package into your new Canvas module, and select the Announcements

## File descriptions
*canvas-announce.py* is the Python source code for the program. You can donwload and run this in your own Python environment.
*canvas-announce.exe* is a standalone executable file for Windows PC, compiled using PyInstaller, that can be downloaded and run without needing a Python installation.

## What is the program doing?
This program parses and edits a course export package from Canvas to allow you to more easily edit and schedule course announcements. It requires a course export in .imscc format. It identifies announcements within that package, and summarises them in a CSV file for editing. Once ypou have edited the announcements, it then re-packages them back into the .imscc file for re-importing to Canvas. It only edits the announcement files, and all other files are retained unedited.

## Limitations
The program does not currently allow you to create new course packages, or to add announcements to a course package.  It only allows the editing (or removal) of existing announcements that you have exported from a course.

## More detail
### Announcement Titles
These should be entered in plain text.
e.g. ```First Teaching Day this Saturday```
### Announcement text
These shoudl be entered using html tags.  This allows links and some basic formatting of messages.
e.g. ```<p>Just a quick reminder about the upcoming Day 3 this Saturday 4th November.  Please do try and download the files in advance of the class if you can.  We will begin at 10:15am as usual in 2Y5.</p>
<p>See you all on Saturday.</p>```
### Delay dates
These need to be entered in the format YYYY-MM-DDTHH:MM:SS
Note that years are four digits, months and days are two digits (i.e. include leading zeroes) and the time is in the 24 clock (include leading zeroes). Note also the character 'T' separating the date and the time.
Examples:
```2018-11-29T15:00:00```
```2018-12-10T10:00:00```
