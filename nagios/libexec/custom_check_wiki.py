#!/usr/bin/env python

import sys, getopt
import twill.commands

nagios_codes = {'OK': 0,
                'WARNING': 1,
                'CRITICAL': 2,
                'UNKNOWN': 3,
                'DEPENDENT': 4}

def usage():
    """ returns nagios status UNKNOWN with
        a one line usage description
        usage() calls nagios_return()
    """
    nagios_return('UNKNOWN',
            "usage: %s -s <wiki_url> -u <username> -p <password>" % sys.argv[0])

def nagios_return(code, response):
    """ prints the response message
        and exits the script with one
        of the defined exit codes
        DOES NOT RETURN
    """
    print code + ": " + response
    sys.exit(nagios_codes[code])

def check_condition(url, user, password):
	a = twill.commands
	a.redirect_output("/dev/null")
	a.config("readonly_controls_writeable", 1)
	b = a.get_browser()
	b.clear_cookies()
	result = b.go(url)
	a.fv(1, "wpName", user)
	a.fv(1, "wpPassword", password)
	b.submit()
	try:
		a.find("Welcome to the Wiki")
		return {"code": "OK", "message": "Successfully logged into the wiki."}
	except:
		return {"code": "CRITICAL", "message": "Unable to login to the wiki!"}

def main():
	if len(sys.argv) < 2:
		usage()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "s:u:p:")
	except getopt.GetoptError, err:
		usage()

	for o, value in opts:
		if o == "-s":
			URL = value
		elif o == "-u":
			USER = value
		elif o == "-p":
			PASS = value
		else:
			usage()

	result = check_condition(URL, USER, PASS)
	nagios_return(result['code'], result['message'])

if __name__ == "__main__":
    main()
