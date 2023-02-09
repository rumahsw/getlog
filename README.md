# getlog

getlog akan membaca dan memparsing baris per baris dari nginx error log file. Kemudian mengekstrak data-data timestamp, severity, process_id, thread_id, connection_id, message, client_ip, request, server, dan host. Lalu merubah ke format json.

Contoh penggunaan:
```
python3 getlog.py inputsample_error.log -t json -o nginx_error_log.json
```
atau
```
python3 getlog.py -h
```

tested on Python 3.8.10
