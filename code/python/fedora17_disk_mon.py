#!/usr/bin/env python
import os
import sys

smart_conf = """
DEVICESCAN -a -H -t -I 194 -W 4,40,50 -R 5 -o on -S on -s (S/../.././02|L/../../6/03) -n standby -m hcpinfrastructure@hds.com -M diminishing -M exec /data/scripts/waltham_smartd_error_report.sh
"""

smart_script = """
#! /bin/bash

# Save the email message (STDIN) to a file:
cat > /tmp/smartd_errorMsg.log
echo >> /tmp/smartd_errorMsg.log
echo "-----------------------------------------------------------" >> /tmp/smartd_errorMsg.log
echo >> /tmp/smartd_errorMsg.log

# Make sure we figure out what host this is coming from
echo "Hostname=`hostname`" >> /tmp/smartd_errorMsg.log
echo >> /tmp/smartd_errorMsg.log

echo "ifconfig=" >> /tmp/smartd_errorMsg.log
/sbin/ifconfig 2>&1 >> /tmp/smartd_errorMsg.log
echo >> /tmp/smartd_errorMsg.log

echo "Machine Type=`/usr/sbin/dmidecode --string system-manufacturer` `/usr/sbin/dmidecode --string system-product-name`" >> /tmp/smartd_errorMsg.log
echo >> /tmp/smartd_errorMsg.log

echo "Directory list of /home - to determine usernames" >> /tmp/smartd_errorMsg.log
ls -1 --color=never /home 2>&1 >> /tmp/smartd_errorMsg.log
echo >> /tmp/smartd_errorMsg.log


echo >> /tmp/smartd_errorMsg.log
echo "-----------------------------------------------------------" >> /tmp/smartd_errorMsg.log
echo >> /tmp/smartd_errorMsg.log

env >> /tmp/smartd_errorMsg.log

echo >> /tmp/smartd_errorMsg.log
echo "-----------------------------------------------------------" >> /tmp/smartd_errorMsg.log
echo >> /tmp/smartd_errorMsg.log

echo "fdisk -l" >> /tmp/smartd_errorMsg.log
/sbin/fdisk -l 2>&1 >> /tmp/smartd_errorMsg.log

echo "df -h" >> /tmp/smartd_errorMsg.log
/bin/df -h 2>&1 >> /tmp/smartd_errorMsg.log

echo >> /tmp/smartd_errorMsg.log
echo "-----------------------------------------------------------" >> /tmp/smartd_errorMsg.log
echo >> /tmp/smartd_errorMsg.log

# Append the output of smartctl -a to the message:
echo "Running smartctl: /usr/sbin/smartctl -a -d $SMART_DEVICETYPE $SMARTD_DEVICE" >> /tmp/smartd_errorMsg.log

echo /usr/sbin/smartctl -a -d $SMARTD_DEVICETYPE $SMARTD_DEVICE >> /tmp/test.log
/usr/sbin/smartctl -a -d $SMARTD_DEVICETYPE $SMARTD_DEVICE >> /tmp/smartd_errorMsg.log



# Warn all users of a problem
wall <<EOF
Problem detected with disk: $SMARTD_DEVICE
Warning message from smartd is: $SMARTD_MESSAGE
See DevOps Team for assistance.
EOF

/usr/bin/notify-send --expire-time=259200000 --urgency=critical "Problem detected with disk: $SMARTD_DEVICE"  "Problem detected with disk: $SMARTD_DEVICE"

# Now email the message to the user at address ADD:
echo /bin/mail -r hcpinfrastructure@hds.com -s "$SMARTD_SUBJECT" -S "smtp=smtp://mail.archivas.com" $SMARTD_ADDRESS >> /tmp/test.log
/bin/mail -r hcpinfrastructure@hds.com -s "$SMARTD_SUBJECT" -S "smtp=smtp://mail.archivas.com" $SMARTD_ADDRESS < /tmp/smartd_errorMsg.log

"""

desktop_info_script = """
#!/bin/bash
/usr/bin/curl -ivX DELETE --stderr - http://infrastructure.engineering.ark.archivas.com/rest/desktop_info/`hostname -s`.json &>/dev/null
/usr/bin/curl -ivX DELETE --stderr - http://infrastructure.engineering.ark.archivas.com/rest/desktop_info/`hostname -s`.html &>/dev/null

cd /tmp ; lshw -json > /tmp/`hostname -s`.xml ; curl -T /tmp/`hostname -s`.xml http://infrastructure.engineering.ark.archivas.com/rest/desktop_info/`hostname -s`.json ; rm /tmp/`hostname -s`.xml &>/dev/null
cd /tmp ; lshw -html > /tmp/`hostname -s`.html ; curl -T /tmp/`hostname -s`.html http://infrastructure.engineering.ark.archivas.com/rest/desktop_info/`hostname -s`.html ; rm /tmp/`hostname -s`.html &>/dev/null
"""


def install_tools():
    print('installing the smart tools via yum')
    os.system('yum install smartmontools lshw curl -y')
    print('Done installing smart tools')


def install_smart_script():
    if not os.path.isdir('/data/scripts'):
        os.makedirs('/data/scripts')
    with open('/data/scripts/waltham_smartd_error_report.sh', 'w') as scriptfile:
        scriptfile.write(smart_script)
    os.chmod('/data/scripts/waltham_smartd_error_report.sh', 0755)


def smartmon_config():
    print('Writing out the smart config file')
    with open('/etc/smartd.conf', 'w') as conf_file:
        conf_file.write(smart_conf)
    print('Done writing the config file.')


def install_desktop_cron():
    print('Adding cron')
    with open('/etc/cron.monthly/desktop_info.sh', 'w') as desktop_file:
        desktop_file.write(desktop_info_script)
    os.chmod('/etc/cron.monthly/desktop_info.sh', 0755)
    print('Done adding cron')


def restart_smart_service():
    print('Restarting smartmon service')
    os.system('systemctl restart smartd.service')


if __name__ == '__main__':
    if os.geteuid():
        print('Need to run as root!')
        sys.exit(1)
    install_tools()
    install_smart_script()
    smartmon_config()
    install_desktop_cron()
    restart_smart_service()
    print('Finished Script!')
