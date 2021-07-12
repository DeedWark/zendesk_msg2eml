# zendesk_msg2eml
Convert MSG to EML in Zendesk Tickets

## Init
!!! Change value into app/config.txt

## Launch
```bash
python3 zendesk_msg2eml.py
```

# Docker

- Build
```bash
docker build --build-arg ZENDESK_TOKEN="<yourtoken>" -t zendesk_msg2eml .
# OR
export ZENDESK_TOKEN="<yourtoken>"
docker build --build-arg ZENDESK_TOKEN -t zendesk_msg2eml .
```

- Run

```bash
docker run -d --name zendesk_msg2eml zendesk_msg2eml
```
