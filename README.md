# zendesk_msg2eml
Convert MSG to EML in Zendesk Tickets
## Init


1 - Don't forget to change values into app/config.txt

2 - Create a Zendesk View -> contains none of the following tags: `msg2eml_done`, `msg2eml_failed`

- Zendesk Email, Zendesk Subdomain, Zendesk view_id, Zendesk author_id, MSG directory = app/config.txt
> Example:
```
[ZENDESK]
email=user@email.com
subdomain=mycompany
view_id=1234567
author_id=9876543

[SYSTEM]
directory=msg
```
- Zendesk Token = environment variable -> ZENDESK_TOKEN
> Example:
```bash
export ZENDESK_TOKEN="1234567abcdef"
```

- If you want to launch directly this script in your host, make sure you have mapitool installed -> `apt install rubygems gems && gem install ruby-msg`
```
python3 app/zendesk_msg2eml.py
```

## Docker

- Build
```
docker build --build-arg ZENDESK_TOKEN="<yourtoken>" -t zendesk_msg2eml .
# OR
export ZENDESK_TOKEN="<yourtoken>"
docker build --build-arg ZENDESK_TOKEN -t zendesk_msg2eml .
```

- Run


```
docker run -d --name zendesk_msg2eml zendesk_msg2eml
```
____


## Infos

- I choose mapitool from ruby-msg because this tool is able to convert HTML/CSS instead of others scripts
