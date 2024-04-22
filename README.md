# Cloud-Diagnostics
Cloud diagnostics on a particular website and a down-detector that sends email if it has been down for a certain period of time

Configuration Steps:
1. Add email login credentials to src\private\smtp_credentials.txt, matching the template format provided in src\private\smtp_credentials_template.txt
2. Set the receiver email in src\script.py send_email()
3. Set the downtime_threshold in src\script.py such that a downtime_threshold of 23 hours will notify the host if the server is down in 23-24hours (assuming hourly crontab)
4. Ensure the sender credentials are accurate, Gmail will require configuring an "App" password that is independent to the traditional password
5. Move src\script.py and src\private to the server that will monitor the site. 
6. Set the url of the site in src\script.py url_to_monitor parameter
7. src\index.html is just a sample site that can be used, though it does not need to be hosted in the same server that runs the script.
8. Run script.py to check if the server is down. Run the script repeatedly until it has been down for 23-24+ hours
9. Alternatively, setup a crontab to run the script passively, such as 0 * * * * sudo /usr/bin/python3 /scripts/script.py, which runs at the beginning of every hour