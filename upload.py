#!/usr/bin/env python
import os, re, sys
from os.path import join, abspath, isfile, isdir, exists, basename
from shutil import copyfile, copytree, rmtree
from time import strftime, strptime, localtime
from simplejson import dumps, loads
from optparse import OptionParser
parser = OptionParser()

try:
    # maybe you don't have Jinja2?
    from config import config
except:
    print "No config file found: 'config.py'."
    sys.exit(0)

def p(o):
    return dumps(o, indent=4)

sys.path.append(join(abspath('.'), 'src'))
from amo import AMOAuth

if __name__ == '__main__':

    parser.add_option("-u",
                      "--user",
                      dest="user_id",
                      help="the unique user id for the target user.",
                      )

    parser.add_option("-f",
                      "--xpi",
                      dest="xpi",
                      help="the xpi file to upload.",
                      )

    parser.add_option("-i",
                      "--addon",
                      dest="addon",
                      help="the addon id to update.",
                      )

    (options, args) = parser.parse_args()

    if not options.xpi:
        parser.error('A filename is required')

    if not exists(options.xpi):
        parser.error("File doesn't exist? %s" % options.xpi)

    if not options.user:
        parser.error('A user id is required')

    if not options.addon:
        parser.error('An addon id is required')

    xpi_file = open(options.xpi, 'rb')
    endpoint = config['endpoint']

    amo = AMOAuth(domain=endpoint['domain'], port=endpoint['port'], protocol=endpoint['protocol'])

    amo.set_consumer(consumer_key=config['consumer_key'],
                         consumer_secret=config['consumer_secret'])
    user = amo.get_user()

    data = {
        'xpi': xpi_file, 
        'authenticate_as': user['id'],
        'release_notes': 'Uploaded by the awesome uploader!'
    }

    print options.addon
    response = amo.create_version(data, options.addon)
