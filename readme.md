# Attachment2Nexcloud

The script fetches the attachments of a imap-mailbox and uploads the files to a nextcloud-storage. 

To prevent overwriting of existings files a timestamp will be added to the filename. 

## Requirements
```
pip install imap_tools
pip install pyocclient
pip install pytz
```

## Usage
```
py.exe attachment2nextcloud.py
```