#!/usr/bin/env python
from __future__ import absolute_import
import httplib2
import pprint
import sys
import os
import logging

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets

def main(args):
	src_dir = args[1]
	if not os.path.exists(src_dir) or not os.path.isdir(src_dir):
		print "Directory not found: \"%s\"" % src_dir
		return

	logging.basicConfig(level=logging.ERROR)
	# Run through the OAuth flow and retrieve credentials
	flow = flow_from_clientsecrets(	'client_secrets.json',
									scope='https://www.googleapis.com/auth/drive',
									redirect_uri='urn:ietf:wg:oauth:2.0:oob')
	authorize_url = flow.step1_get_authorize_url()
	print 'Go to the following link in your browser: ' + authorize_url
	code = raw_input('Enter verification code: ').strip()
	credentials = flow.step2_exchange(code)	

	# Create an httplib2.Http object and authorize it with our credentials
	http = httplib2.Http()
	http = credentials.authorize(http)

	drive_service = build('drive', 'v2', http=http)

	allow_file = [".py"]

	print "Start uploading..."
	dir_mime = "application/vnd.google-apps.folder"
	app_name = "code2pdf"
	query_str = "title='%s' and mimeType='%s'" % (app_name, dir_mime)
	remote_dir = drive_service.files().list(q=query_str).execute()
	if 	len(remote_dir["items"]) == 0 or\
		("labels" in remote_dir["items"][0] and remote_dir["items"][0]["labels"]["trashed"]):
		remote_dir = drive_service.files().insert(body={"title":app_name,"mimeType":dir_mime}).execute()
	else:
		remote_dir = remote_dir["items"][0]
	for f in os.listdir(src_dir):
		full_path = os.path.join(src_dir, f)
		if os.path.isfile(full_path) and os.path.splitext(f)[1] in allow_file:
			# Insert a file
			media_body = MediaFileUpload(full_path, mimetype='text/plain', resumable=True)
			body = {
			  'title': f,
			  'mimeType': 'text/plain',
			  "parents": [remote_dir]
			}

			file = drive_service.files().insert(convert=True, body=body, media_body=media_body).execute()
			pprint.pprint(file['exportLinks']['application/pdf'])
	print "...OK"

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage:\n\tcode2pdf.py SOURCE_CODE_DIR"
	else:
		main(sys.argv)