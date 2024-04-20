# Cloud-Diagnostics
Cloud diagnostics on a particular website and a down-detector that sends email if it has been down for a certain period of time

Configuration Steps:
1. Add credentials to src\private\smtp_credentials.txt, matching the template format provided in src\private\smtp_credentials_template.txt
2. Ensure the credentials are accurate, Gmail will require configuring an "App" password that is independent to the traditional password
3. Set the server to ping in src\script.py
4. Run script.py to check if the server is down. Run the script repeatedly until it has been down for 23-24+ hours
5. Alternatively, setup a crontab to run the script passively, such as 0 * * * * sudo /usr/bin/python3 /scripts/script.py, which runs at the beginning of every hour