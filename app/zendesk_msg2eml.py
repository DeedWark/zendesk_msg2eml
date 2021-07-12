import os
import time
import shutil
import requests
import subprocess
import configparser
from zenpy import Zenpy

# CONFIG PARSER
config = configparser.ConfigParser()
config.read('config.txt')
email = config.get('ZENDESK', 'email')
subdomain = config.get('ZENDESK', 'subdomain')
view_id = config.get('ZENDESK', 'view_id')
view_id = int(view_id)
author_id = config.get('ZENDESK', 'author_id')
author_id = int(author_id)
DIR = config.get('SYSTEM', 'directory')
# Env var
token = os.environ.get("ZENDESK_TOKEN")

creds = {
    'email': f"{email}",
    'token': f"{token}",
    'subdomain': f"{subdomain}'
}
zenpy = Zenpy(**creds)

if not os.path.exists(DIR):
    os.mkdir(DIR)
else:
    shutil.rmtree(DIR, ignore_errors=True)
    os.mkdir(DIR)

def msg2eml(view_id):
    """ EXECUTE VIEW IN ORDER TO GET TICKETS """
    for ticket in zenpy.views.tickets(view=view_id):
        ticket_id = ticket.id

        """ GET ALL COMMENT, ALL ATTACHMENTS AND THEIR CONTENT_URL, CONTENT_TYPE AND FILE_NAME """
        for comment in zenpy.tickets.comments(ticket_id):
            for attachment in comment.attachments:
                file_url = attachment.content_url
                file_type = attachment.content_type
                file_name = attachment.file_name
                # Download only MSG file
                if file_type == "application/octet-stream" or file_type == "application/vns.ms-outlook":
                    if file_name.lower().endswith(".msg"):
                        r = requests.get(file_url)
                        open(DIR+f"/{file_name[:-4]}{file_count}.msg", "wb").write(r.content)

        """ CONVERT ALL MSG FILE IN MSG DIR WITH RUBY MSG CONVERTER """
        for file in os.listdir(DIR):
            if file.lower().endswith(".msg"):
                try:
                    subprocess.run(["mapitool", "-i", DIR+"/"+file, "-o", DIR])
                except (RuntimeError, Exception) as err:
                    print(err)
            else:
                pass

        """  UPLOAD EACH EML FILE INTO ITS TICKET AND ADD TAG msg2eml_done """
        from zenpy.lib.api_objects import Comment, Ticket

        for file in os.listdir(DIR):
            if file.lower().endswith(".eml"):
                upload_instance = zenpy.attachments.upload(DIR+"/"+file)
                ticket = zenpy.tickets(id=ticket_id)
                ticket.comment = Comment(
                    body=f"File: {file_name} converted from MSG to EML - New File: {file}",
                    uploads=[upload_instance.token],
                    public=False,
                    author_id=author_id
                    )
                ticket.tags.extend(['msg2eml_done'])
                zenpy.tickets.update(ticket)

        return True

def main():
    while True:
        msg2eml(view_id)
        time.sleep(60)

if __name__ == '__main__':
    main()
