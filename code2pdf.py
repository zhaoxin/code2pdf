#!/usr/bin/env python
from __future__ import absolute_import
import httplib2
import pprint
import sys
import os
import logging
import webbrowser
from apiclient.discovery import build
from apiclient.http 	 import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets


class Code2PDF():
	def __init__(self, src, dest):
		self.src = src;				# source code directory or file
		self.dest = dest;			# where to save converted pdf
		self.service = None;		# google drive api
		self.allow_file = [".py"];	# file type to upload, e.g., [".py",".c",".h"]
		self.remote_root = None;	# remote dir on google drive, i.e., "code2pdf"
		logging.basicConfig(level=logging.ERROR)
	
	def authorize(self):
		# Run through the OAuth flow and retrieve credentials
		flow = flow_from_clientsecrets(	"client_secrets.json",
										scope="https://www.googleapis.com/auth/drive",
										redirect_uri="urn:ietf:wg:oauth:2.0:oob")
		authorize_url = flow.step1_get_authorize_url()
		print "Follow the link in your browser to authorize."
		webbrowser.open(authorize_url)
		code = raw_input("After you're done, enter verification code: ").strip()
		credentials = flow.step2_exchange(code)	
		# Create an httplib2.Http object and authorize it with our credentials
		http = httplib2.Http()
		http = credentials.authorize(http)
		self.service = build("drive", "v2", http=http)

	def process(self):
		print "Processing..."
		self.makeremotedir()
		if os.path.isdir(self.src):
			for f in os.listdir(self.src):
				full_path = os.path.join(self.src, f)
				if os.path.isfile(full_path) and os.path.splitext(f)[1] in self.allow_file: 	
					self.processfile(self.src, f)
		else:
			self.processfile(os.path.dirname(self.src), os.path.basename(self.src))
		print "...Done"

	def processfile(self, folder, fn):
		print "\tProcess \"%s\"..." % fn,
		rslt = ""
		full_path = os.path.join(folder, fn)
		pdf_path = os.path.join(self.dest if self.dest else folder, os.path.splitext(fn)[0]+".pdf")
		media_body = MediaFileUpload(full_path, mimetype="text/plain", resumable=True)
		body = {
		  "title": fn,
		  "mimeType": "text/plain",
		  "parents": [self.remote_root]
		}
		remote_file = self.service.files().insert(convert=True, body=body, media_body=media_body).execute()
		download_url = remote_file['exportLinks']['application/pdf']
		if download_url:
			resp, content = self.service._http.request(download_url)
			if resp.status == 200:
				with open(pdf_path, "wb") as pdf:
					pdf.write(content)
				rslt = "Done"
			else:
				rslt = "Error: %s" % resp
		else:
			# The file doesn't have any content stored on Drive.
			rslt = "Error: Empty file"
		print rslt

	def makeremotedir(self):
		remote_dir = None
		dir_mime = "application/vnd.google-apps.folder"
		app_name = "code2pdf"
		query_str = "title='%s' and mimeType='%s'" % (app_name, dir_mime)
		search = self.service.files().list(q=query_str).execute()	# search "code2pdf" in google drive
		if len(search["items"]) > 0:
			for item in search["items"]:
				if("labels" in item and not item["labels"]["trashed"]):
					remote_dir = item
					break 			
		if remote_dir is not None:
			self.remote_root = remote_dir
		else:
			self.remote_root = self.service.files().insert(body={"title":app_name,"mimeType":dir_mime}).execute()

if __name__ == "__main__":
	args = sys.argv
	start = False
	if len(args) < 2:
		print "Usage:\n\tcode2pdf.py SOURCE_CODE_PATH [PDF_SAVE_PATH]"
	elif not os.path.exists(args[1]):
		print "Directory or file not found: \"%s\"" % args[1]
	elif not os.path.isdir(args[1]) and not os.path.isfile(args[1]):
		print "Unknown resource type: \"%s\"" % args[1]
	elif len(args) > 2 and os.path.exists(args[2]) and not os.path.isdir(args[2]):
		print "PDF path is not directory: \"%s\"" % args[2]
	elif len(args) > 2 and not os.path.exists(args[2]):
		choice = raw_input("Directory not found: \"%s\"\nCreate it and continue?(y/n):" % args[2]).strip()
		if choice.lower().startswith("y"):
			os.mkdir(args[2])
			start = True
	elif not os.path.exists("client_secrets.json"):
		print "Client secret file not found: \"client_secrets.json\""
	else:
		start = True

	if start:
		code2pdf = Code2PDF(args[1], args[2] if len(args) > 2 else None)
		code2pdf.authorize()
		code2pdf.process()
