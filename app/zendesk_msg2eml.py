import os
import time
import shutil
import requests
import subprocess
import configparser
from zenpy import Zenpy

# CONFIG PARSER
config = configparser.ConfigParser()
config.read('/app/config.txt')
email = config.get('ZENDESK', 'email')
subdomain = config.get('ZENDESK', 'subdomain')
view_id = config.get('ZENDESK', 'view_id')
view_id = int(view_id)
author_id = config.get('ZENDESK', 'author_id')
author_id = int(author_id)
DIR = config.get('SYSTEM', 'directory')
# ENV VAR
token = os.environ.get("ZENDESK_TOKEN")

creds = {
    'email': f"{email}",
    'token': f"{token}",
    'subdomain': f"{subdomain}"
}
zenpy = Zenpy(**creds)

def msg2eml(view_id, author_id, DIR):
    if not os.path.exists(DIR):
        os.mkdir(DIR)
    else:
        shutil.rmtree(DIR, ignore_errors=True)
        os.mkdir(DIR)

    """ EXECUTE VIEW IN ORDER TO GET TICKETS """
    for ticket in zenpy.views.tickets(view=view_id):
        ticket_id = ticket.id
        print(f"Ticket available in this view: {ticket_id}")

        """ GET ALL COMMENT, ALL ATTACHMENTS AND THEIR CONTENT_URL, CONTENT_TYPE AND FILE_NAME """
        for comment in zenpy.tickets.comments(ticket_id):
            for attachment in comment.attachments:
                file_url = attachment.content_url
                file_type = attachment.content_type
                file_name = attachment.file_name
                file_count = 0
                # Download only MSG file
                if file_type == "application/octet-stream" or file_type == "application/vns.ms-outlook":
                    if file_name.lower().endswith(".msg"):
                        r = requests.get(file_url)
                        open(DIR+f"/{file_name[:-4]}{file_count}.msg", "wb").write(r.content)
                        file_count += 1

        """ CONVERT ALL MSG FILE IN MSG DIR WITH RUBY MSG CONVERTER """
        for file in os.listdir(DIR):
            if file.lower().endswith(".msg"):
                print(file)
                try:
                    subprocess.check_output(["mapitool", "-i", DIR+"/"+f"{file}", "-o", DIR],
                        stderr=subprocess.STDOUT,
                        shell=False
                    )
                except subprocess.CalledProcessError as err:
                    print(f"Failed to convert {file} MSG to EML, please do it manually!", err)
                    pass
            else:
                pass

        """  UPLOAD EACH EML FILE INTO ITS TICKET AND ADD TAG msg2eml_done """
        from zenpy.lib.api_objects import Comment, Ticket

        for file in os.listdir(DIR):
            if file.lower().endswith(".eml"):
                file_path = DIR+"/"+file
                print(f"File in {file_path}")
                try:
                    upload_instance = zenpy.attachments.upload(file_path)
                    ticket = zenpy.tickets(id=ticket_id)
                    ticket.comment = Comment(
                        body=f"File {file[:-4]}.msg converted from MSG to EML - New File: {file}",
                        uploads=[upload_instance.token],
                        public=False,
                        author_id=author_id
                        )
                    ticket.tags.extend(['msg2eml_done'])
                except:
                    ticket.comment = Comment(
                        body=f"Failed to convert and upload {file[:-4]}.msg from MSG to EML, please try manually!",
                        public=False,
                        author_id=author_id
                    )
                    ticket.tags.extend(['msg2eml_failed'])
                
            zenpy.tickets.update(ticket)

        return True

def main():
    while True:
        msg2eml(view_id, author_id, DIR)
        time.sleep(60)

if __name__ == '__main__':
    main()
    
