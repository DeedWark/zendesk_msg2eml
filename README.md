# zendesk_msg2eml
Convert MSG to EML in Zendesk Tickets

## Init
/!\ Don't forget to change values into app/config.txt

## Launch
- If you want to launch directly this script in your host, make sure you have mapitool installed -> `apt install rubygems gems && gem install ruby-msg`

```
python3 zendesk_msg2eml.py
```

## Zendesk
- Create a view -> contains none of the following tags: msgconverted

## Docker

- Build
```
docker build --build-arg ZENDESK_TOKEN="<yourtoken>" -t zendesk_msg2eml .
# OR
export ZENDESK_TOKEN="<yourtoken>"
docker build --build-arg ZENDESK_TOKEN -t zendesk_msg2eml .
```

-> Run
```
docker run -d --name zendesk_msg2eml zendesk_msg2eml
```
____
## Infos
- I choose mapitool from ruby-msg because this tool is able to convert HTML/CSS instead of others scripts
