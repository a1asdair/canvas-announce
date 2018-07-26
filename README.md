# canvas-announce
This is a simple routine to support the editing and scheduling of announcements in Canvas

## Quick Start
* Export the Canvas course that includes the announcements you want to edit/schedule
* Run canvas-announce.exe in the same directory as the course export. This will create a CSV file called announcements.csv
* Edit the CSV. You can change the title, message and delay fields.
* Use the 'Include' field to indicate which announcements should be imported ('1') and excluded ('0')
* Save the CSV file
* Run canvas-announce.exe again. This will create a Canvas course packagae for import.
* Import the course package into your new Canvas module, and select the Announcements


