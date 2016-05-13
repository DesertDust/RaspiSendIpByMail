__author__ = 'tom'
from urllib import urlopen
import smtplib
import time
import thread
import LCD


def return_ip():
    d = urlopen("http://www.icanhazip.com")
    x = d.read()
    d.close()
    return x


def send_email(message):
    message = message.strip('\n')
    message = 'Subject: Router Has Been Reset' + '\n\n' + \
              time.ctime(time.time()) + '\n' \
                                        '\nIP Address: ' + message + \
              '\nVNC Address: ' + message + ':5911' + \
              '\nSSH Address: ' + message + ':2211' + \
              '\nPrinter Address: ' + message + ':63111'
    fromaddrs = ''
    toaddrs = ''
    username = ''
    password = ''
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        print "Started"
        server.login(username, password)
        print "Logged In!"
        server.sendmail(fromaddrs, toaddrs, message)
        print "Message Sent!"
        server.quit()
        update_log("Sent.")
    except NotImplementedError:
        print "Error: Couldn't Send eMail"
        update_log("Error in sending eMail")


def compare_to_file(ip_address):
    ip = read_ip()
    log = read_log()
    if ip == ip_address and log == 'Sent.':
        print str(time.ctime(time.time())) + ": IP is still:" + ip
    else:
        update_ip(ip_address)
        send_email(ip_address)


def compare_loop():
    while True:
        thread.start_new_thread(compare_to_file, (return_ip(),))
        LCD.lcdPrinter("Tom Giro", 2)
        LCD.lcdPrinter("IP:" + urlopen("http://www.icanhazip.com/s").read(), 1)
        time.sleep(5 * 60)


def read_ip():
    ip_read = open("/home/pi/Desktop/RaspiSendEmail/ip.txt", "r")
    ip = ip_read.read()
    ip_read.close()
    return ip


def read_log():
    log_read = open("/home/pi/Desktop/RaspiSendEmail/log.txt", "r")
    log = log_read.read()
    log_read.close()
    return log


def update_ip(ip_address):
    ip_write = open("/home/pi/Desktop/RaspiSendEmail/ip.txt", "w")
    ip_write.write(ip_address)
    ip_write.close()
    print 'Updated IP'


def update_log(message):
    log_write = open("/home/pi/Desktop/RaspiSendEmail/log.txt", "w")
    log_write.write(message)
    log_write.close()
    print 'Updated log to:' + message


# noinspection PyBroadException
def main():
    try:
        LCD.initialization()
        compare_loop()

        return None
    except KeyboardInterrupt:
        print "Ended by user."
    except:
        try:
            print "Whoops! An exception.. Restarting"
            time.sleep(2.5 * 60)
            main()
        except:
            pass


if __name__ == '__main__':
    main()
