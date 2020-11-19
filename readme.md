# Attachment2Nexcloud
Das Script greift auf ein IMAP-Postfach zu und lädt die Anhänge der Email-Nachrichten, die seit der letzen Ausführung des Skriptes eingetroffen sind, auf eine Nextcloud hoch. 

Damit keine Dateien in der Cloud überschrieben werden, wird in den Dateinamen der hochgeladenen Dateien ein Timestamp angehängt. 

## Voraussetzungen
```
pip install imap_tools
pip install pyocclient
pip install pytz
```

## Verwendung
```
py.exe attachments2nextcloud.py
```
