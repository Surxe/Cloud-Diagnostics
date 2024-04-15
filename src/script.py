import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os

# URL to monitor
url_to_monitor = 'HTTP://18.220.54.59'
#smtp_credentials_file = 'src/private/smtp_credentials.txt'
script_directory = os.path.dirname(os.path.abspath(__file__))
smtp_credentials_file = os.path.join(script_directory, 'private', 'smtp_credentials.txt')
log_directory = os.path.join(script_directory, 'logs')

# Function to check the URL
def check_url(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return False, response.status_code
        return True, response.status_code
    except requests.ConnectionError:
        return False, "Connection Error"

# Function to send email
def send_email(error_code, error_message):
    receiver_email = 'your.server.is.down.24hrs@gmail.com'
    subject = f"Web Server Error {error_code}"
    body = f"Error {error_code}, {error_message}, detected {datetime.now().strftime('%d %b. %Y, %I:%M%p %Z')}"
    
    message = MIMEText(body)
    message['Subject'] = subject
    message['To'] = receiver_email
    
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Send email
    try:
        with open(smtp_credentials_file) as f:
            smtp_username = ''
            smtp_password = ''
            for line in f:
                key, value = line.strip().split(':', 1)
                if key.strip() == 'username':
                    smtp_username = value.strip()
                elif key.strip() == 'password':
                    smtp_password = value.strip()
    
        message['From'] = smtp_username
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, receiver_email, message.as_string())
        server.quit()
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

# Main function to monitor and send email
def main():
    # If credentials file does not exist, end program and refer user to the template
    if not os.path.exists(smtp_credentials_file):
        print(f"Please create SMTP credentials file at {smtp_credentials_file} with your SMTP credentials in the format shown in /src/private/smtp_credentials_template.txt.")
        return

    # Directory to store last email timestamp
    os.makedirs(log_directory, exist_ok=True)
    log_file = os.path.join(log_directory, 'timestamp.txt')

    # Load last email timestamp
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            timestamp_str = f.read()
            if timestamp_str == '':
                timestamp = ''
            else:
                timestamp = datetime.fromisoformat(timestamp_str)
    else:
        timestamp = ''

    # Check if server is up and get error code
    is_up, error_code = check_url(url_to_monitor)

    # Determine time threshold for email notification
    time_threshold_hours = 23
    current_time = datetime.now().isoformat()
    if timestamp == '':
        exceeds_time_threshold = False
    else:
        exceeds_time_threshold = timestamp < (datetime.now() - timedelta(hours=time_threshold_hours))
    

    # If server is online, send no email and set the log to empty ''
    # Once server is detected to be offline, save the time it went offline in the logs if there is no time logged
    # If there is a time logged, check if it has been 24 hours and if so, send an email and reset the log to ''
    # This way, email will be resent every 24 hours until the server is back online
    
    # If server is offline
    if not is_up:
        if timestamp == '':
            new_log_text = current_time #set log to current time
        elif exceeds_time_threshold:
            send_email(error_code, f"Server is down for more than {time_threshold_hours} hours.")
            new_log_text = '' #reset log to empty to allow for next email in another threshold
        else:
            new_log_text = timestamp.isoformat() #dont change the log
    else:
        new_log_text = '' #server is online so log doesnt matter, make it empty

    # Save the new log text to file for debugging
    with open(log_file, 'w') as f:
        f.write(new_log_text)

    # output = f"Web server is up?: {is_up}\n" \
    #          f"Response code: {error_code}\n" \
    #          f"Current timestamp: {timestamp}\n" \
    #          f"New timestamp: {new_log_text}\n" \
    #          f"Has it been {time_threshold_hours} hours since the server went down? {exceeds_time_threshold}\n"
    # # Write output to logs
    # with open(os.path.join(log_directory, 'output.txt'), 'a') as f:
    #     f.write(output)

    # Debugging
    # print(f"Web server is up?: {is_up}", 
    #       f"Response code: {error_code}", 
    #       f"Current timestamp: {timestamp}",
    #       f"New timestamp: {new_log_text}",
    #       f"Has it been {time_threshold_hours} hours since the server went down? {exceeds_time_threshold}", 
    #       sep='\n', end='\n\n')

if __name__ == "__main__":
    main()
