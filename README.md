# zendesk_msg2eml
Convert MSG to EML in Zendesk Tickets

## Init
/!\ Don't forget to change values into app/config.txt

-> Launch
- If you want to launch directly this script in your host, make sure you have mapitool installed -> `apt install rubygems gems && gem install ruby-msg`

```bash
python3 zendesk_msg2eml.py
```

## Docker

-> Build
```bash
docker build --build-arg ZENDESK_TOKEN="<yourtoken>" -t zendesk_msg2eml .
# OR
export ZENDESK_TOKEN="<yourtoken>"
docker build --build-arg ZENDESK_TOKEN -t zendesk_msg2eml .
```

-> Run

```bash
docker run -d --name zendesk_msg2eml zendesk_msg2eml
```
