## Instructions for set up and how to run SASSIE insitu data code. 

Main code is plotSuite.py, which collects, plots and writing out to excel files.

Clone this repository. 

Edit the input_args_SASSIE.txt file, changing the --base_dir to your directory. 
You’ll need subdirectories under the base_dir: 
BuoyData/, SatelliteFields/, excel_files/, figs/, pyfiles/, swift_telemetry/, waveGlider/
	under SatelliteFields/ you’ll need Bremen_SIC/, NOAA_SST/, JPL_SMAP/

Setup a cron job to run the code every three hours. In your terminal window

1. type crontab -e		(opens a vi editor window)
2. type i	    		  (changes editor to ‘insert’ or edit mode)
3. copy/paste your version of the following line into the vi editor window:
0 */3 * * * /Users/suzanne/opt/miniconda3/bin/python /Users/suzanne/SASSIE/pyfiles/plotSuite.py @/Users/suzanne/SASSIE/pyfiles/input_args_SASSIE.txt 2>&1 | mail -s "plotSuite" sdickins@uw.edu

4. press escape key	(gets the editor out of edit mode)
5. type :wq		(saves the file)
6. press enter		(closes the vi window)

Explanation of crontab line:
* '0'	run job first minute of the hour
* '*/3'	run job every third hour
* '*'	run every day
* '*'	run every month
* '*'	run every day of the week
* the path to python	(can find with ‘which python’ in terminal window)
* the command, here, the python code and the arguments file (which follows an @)
* 2>&1	this has something to do with debug comments, I think. 
* | mail 	(pipe to mail), sends an email after running
* -s “plotSuite”	let’s you put in whatever subject you want for the email
* lastly 		your email address.


