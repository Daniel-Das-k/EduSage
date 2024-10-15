import os
import random
import sys
import time
import http.client as httplib
import httplib2
from .crew import YouTubeDescriptCreator, YouTubeTitleCreator
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

httplib2.RETRIES = 1

MAX_RETRIES = 10

RETRIABLE_EXCEPTIONS = (
    httplib2.HttpLib2Error, IOError, httplib.NotConnected,
    httplib.IncompleteRead, httplib.ImproperConnectionState,
    httplib.CannotSendRequest, httplib.CannotSendHeader,
    httplib.ResponseNotReady, httplib.BadStatusLine
)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = "youtube_creds.json"

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

description = YouTubeDescriptCreator()
title = YouTubeTitleCreator()

class YouTubeUploader:
    def __init__(self):
        self.args = self.parse_arguments()
        self.title = None
        self.description = None

    def parse_arguments(self):
        argparser.add_argument("--category", default="22", help="Numeric video category. See https://developers.google.com/youtube/v3/docs/videoCategories/list")
        argparser.add_argument("--keywords", help="Video keywords, comma separated", default="")
        argparser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES, default=VALID_PRIVACY_STATUSES[0], help="Video privacy status.")
        return argparser.parse_args()

    def set_content(self, title, description):
        self.title = title
        self.description = description

    def get_authenticated_service(self):
        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE, message=MISSING_CLIENT_SECRETS_MESSAGE)
        storage = Storage("%s-oauth2.json" % sys.argv[0])
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage, self.args)

        return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))

    def initialize_upload(self, youtube, video_file):
        tags = None
        if self.args.keywords:
            tags = self.args.keywords.split(",")

        body = dict(
            snippet=dict(
                title=self.title,
                description=self.description,
                tags=tags,
                categoryId=self.args.category
            ),
            status=dict(
                privacyStatus=self.args.privacyStatus
            )
        )

        insert_request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
        )

        self.resumable_upload(insert_request)

    def resumable_upload(self, insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print("Uploading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print("Video id was successfully uploaded: %s" % response['id'])
                    else:
                        exit("The upload failed with an unexpected response: %s" % response)
            except HttpError as e:
                if e.resp.status == 403 and 'quotaExceeded' in e.content.decode():
                    print("Quota exceeded. Please try again later.")
                    time.sleep(3600)
                    continue
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
                else:
                    raise
            except RETRIABLE_EXCEPTIONS as e:
                error = "A retriable error occurred: %s" % e

            if error is not None:
                print(error)
                retry += 1
                if retry > MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)

    def upload(self, video_file):
        if not os.path.exists(video_file):
            exit("Please specify a valid file path for the video file.")
        
        youtube_service = self.get_authenticated_service()
        try:
            self.initialize_upload(youtube_service, video_file)
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))



##################### Need to do for Demo #############################

# import http.client as httplib
# import httplib2
# import os
# import random
# import sys
# import time
# from .crew import YouTubeDescriptCreator,YouTubeTitleCreator
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from googleapiclient.http import MediaFileUpload
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.file import Storage
# from oauth2client.tools import argparser, run_flow


# httplib2.RETRIES = 1

# MAX_RETRIES = 10

# RETRIABLE_EXCEPTIONS = (
#     httplib2.HttpLib2Error, IOError, httplib.NotConnected,
#     httplib.IncompleteRead, httplib.ImproperConnectionState,
#     httplib.CannotSendRequest, httplib.CannotSendHeader,
#     httplib.ResponseNotReady, httplib.BadStatusLine
# )

# RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# CLIENT_SECRETS_FILE = "youtube_creds.json"

# YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
# YOUTUBE_API_SERVICE_NAME = "youtube"
# YOUTUBE_API_VERSION = "v3"

# MISSING_CLIENT_SECRETS_MESSAGE = """
# WARNING: Please configure OAuth 2.0

# To make this sample run you will need to populate the client_secrets.json file
# found at:

#    %s

# with information from the API Console
# https://console.cloud.google.com/

# For more information about the client_secrets.json file format, please visit:
# https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
# """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
#                                    CLIENT_SECRETS_FILE))

# VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

# description = YouTubeDescriptCreator()
# title = YouTubeTitleCreator()
# class YouTubeUploader:
#     def __init__(self):
#         self.args = self.parse_arguments()
#         self.title = None
#         self.description = None

#     def parse_arguments(self):
#         argparser.add_argument("--category", default="22", help="Numeric video category. See https://developers.google.com/youtube/v3/docs/videoCategories/list")
#         argparser.add_argument("--keywords", help="Video keywords, comma separated", default="")
#         argparser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES, default=VALID_PRIVACY_STATUSES[0], help="Video privacy status.")
#         return argparser.parse_args()

#     def set_content(self, title, description):
#         self.title = title
#         self.description = description

#     def get_authenticated_service(self):
#         flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE, message=MISSING_CLIENT_SECRETS_MESSAGE)
#         storage = Storage("%s-oauth2.json" % sys.argv[0])
#         credentials = storage.get()

#         if credentials is None or credentials.invalid:
#             credentials = run_flow(flow, storage, self.args)

#         return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))

#     def initialize_upload(self, youtube, video_file):
#         tags = None
#         if self.args.keywords:
#             tags = self.args.keywords.split(",")

#         body = dict(
#             snippet=dict(
#                 title=self.title,
#                 description=self.description,
#                 tags=tags,
#                 categoryId=self.args.category
#             ),
#             status=dict(
#                 privacyStatus=self.args.privacyStatus
#             )
#         )

#         insert_request = youtube.videos().insert(
#             part=",".join(body.keys()),
#             body=body,
#             media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
#         )

#         self.resumable_upload(insert_request)

#     def resumable_upload(self, insert_request):
#         response = None
#         error = None
#         retry = 0
#         while response is None:
#             try:
#                 print("Uploading file...")
#                 status, response = insert_request.next_chunk()
#                 if response is not None:
#                     if 'id' in response:
#                         print("Video id was successfully uploaded: %s" % response['id'])
#                     else:
#                         exit("The upload failed with an unexpected response: %s" % response)
#             except HttpError as e:
#                 if e.resp.status == 403 and 'quotaExceeded' in e.content.decode():
#                     print("Quota exceeded. Please try again later.")
#                     time.sleep(3600)  # Sleep for an hour before retrying
#                     continue
#                 if e.resp.status in RETRIABLE_STATUS_CODES:
#                     error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
#                 else:
#                     raise
#             except RETRIABLE_EXCEPTIONS as e:
#                 error = "A retriable error occurred: %s" % e

#             if error is not None:
#                 print(error)
#                 retry += 1
#                 if retry > MAX_RETRIES:
#                     exit("No longer attempting to retry.")

#                 max_sleep = 2 ** retry
#                 sleep_seconds = random.random() * max_sleep
#                 print("Sleeping %f seconds and then retrying..." % sleep_seconds)
#                 time.sleep(sleep_seconds)

#     def upload(self, video_file):
#         if not os.path.exists(video_file):
#             exit("Please specify a valid file path for the video file.")

#         youtube_service = self.get_authenticated_service()
#         try:
#             self.initialize_upload(youtube_service, video_file)
#         except HttpError as e:
#             print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))




