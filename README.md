code2pdf
========

<<<<<<< HEAD
Convert source code files to PDF with Google Drive API.  
Source code files are uploaded to Google Drive and downloaded back to local computer as PDF files.

#### How to use
##### 1. Install Python
  

##### 2. Install Google Drive SDK  

- Follow Step1 and Step2 on this page:  
[https://developers.google.com/drive/quickstart-python](https://developers.google.com/drive/quickstart-python)  

- Download client_secrets.json generated in Step1 from Google APIs Console to your code2pdf directory

##### 3. Config & Run

- Open code2pdf.py and find "self.allow_file = [".py"];". Edit the items in [] to allow file types you want to convert.  
For example, for C language and its header file:
		
		self.allow_file = [".c",".h"];

- Change directory to code2pdf and run:  
	
		python code2pdf.py FILE_OR_DIRECTORY_OF_SOURCE_CODE [DIRECTORY_TO_KEEP_PDF]

	+ FILE\_OR\_DIRECTORY\_OF\_SOURCE\_CODE:  
	**Required**  
	The source code file(s) to be converted.  
	If this is a directory, all the allowed files in it, only root level however, will be converted.   

	+ DIRECTORY\_TO\_KEEP\_PDF:  
	**Optional**  
	The directory to keep downloaded PDF files.  
	If this is not provided, converted PDF files will be downloaded to "pdf" in code2pdf directory.

	Follow the authorizing webpage to allow code2pdf upload source code files to and download converted PDF files from your Google Drive.  
	Copy the verification code from browser back to script, press ENTER, and let code2pdf do all the rest of the work.   

#### Note
The script will create a folder named "code2pdf" in your Google Drive and do all the conversion work in it. You can remove it as you like and the script will create it at next run time. 
=======
Convert source code to PDF with Google Drive API
>>>>>>> 0b3b832f41581520baddaf1d12029f2af2c6afc1
