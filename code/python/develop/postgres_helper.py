#!/usr/bin/env python
# coding=utf-8
import argparse
import logging
import datetime
import sys
import os

from fabric.api import local

__author__ = 'jbean'

# change these as appropriate for your platform/environment :
USER = "postgres"
PASS = ""
HOST = "localhost"

PGPASS_FILE = os.path.normpath('/home/jbean/.pgpass')

DB_MAP = {
    'sprite': 'pxe.archivas.com',
    'tts': 'tts.mcp.com',
}

DB_CONFIG_MAP = {
    'ucptts': {
        'db_host': 'mcp-tts-01',
        'db_name': 'tts',
        'db_user': 'postgres',
        'db_pass': '',
    },
    'hcptts': {
        'db_host': 'db1',
        'db_name': 'tts',
        'db_user': 'postgres',
        'db_pass': '',
    },
    'sprite': {
        'db_host': 'pxe.archivas.com',
        'db_name': 'sprite',
        'db_user': 'postgres',
        'db_pass': '',
    },
}

DUMP_DIR = os.path.normpath('/data/dbdumps')

parser = argparse.ArgumentParser()
sub_parser = parser.add_subparsers(help='Top Level Commands', dest='command')

backup_parser = sub_parser.add_parser('backup', help='Helper functions for backing up a Postgres server')
backup_parser.add_argument('upload_url', help='Target URL to upload the resulting backup.')

parser.add_argument('--host', default=None, help='The production host server running postgres for the '
                                                 'Database you want to dump.')
parser.add_argument('--port', default=5432, help='The production port server running postgres for the Database '
                                                 'you want to dump.')
parser.add_argument('--user', default=USER, help='The postgres user that can do a pg_dump.')
parser.add_argument('--password', default=PASS, help='The user password for performing the pg_dump.')
parser.add_argument('--dump_dir', default=DUMP_DIR, help='directory to put the PG dump files locally.')

clone_parser = sub_parser.add_parser('clone', help='Clone a production DB into a development DB.')

clone_parser.add_argument('--dev_host', default=HOST, help='The host you want to publish the new dev database to.')
clone_parser.add_argument('--dev_port', default=5432, help='The postgres port server running postgres for the '
                                                           'Database you want to clone.')
clone_parser.add_argument('--dev_user', default=USER, help='The postgres user that can do a pg_dump.')
clone_parser.add_argument('--dev_password', default=PASS, help='The user password for performing the pg_dump.')

clone_parser.add_argument('--local', '-l', default=False, action='store_true',
                          help='If you want to use the latest local dump.')

parser.add_argument('database', help='The database name you want to clone.')

FORMAT = "%(asctime)s %(levelname)-6s line %(lineno)-4s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


def pg_dump(host, port, user, database, dump_file_name):
    """
    /usr/bin/pg_dump -h db1 -U postgres jiradb2 -f $BKROOT.$SUF -F c --oids
    >>$LOGFILE 2>&1
    """
    logging.info('Dumping database to file: [{}]'.format(dump_file_name))
    cmd = '/usr/bin/pg_dump -h {host} -p {port} -U {user} {dbname} -f {file} ' \
          '-F c --oids --verbose '.format(host=host, port=port, user=user,
                                          dbname=database, file=dump_file_name)

    local(cmd)


def delete_local_db(local_host, local_port, local_user, new_dev_database):
    """
    locally drop the database that you will be restoring to
    """
    cmd = '/usr/bin/dropdb --host {h} -p {p} -U {u} {db} --if-exists'.format(
        h=local_host, p=local_port, u=local_user, db=new_dev_database)
    local(cmd)


def create_pg_pass_file(host, port, database, user, password):
    """
    Creates the pgpass file in your home dir for re-use and no password
    prompts

    http://www.postgresql.org/docs/8.1/static/libpq-pgpass.html
    """
    logging.info('Writing a pgpass file for connections to the PGDB.')
    pg_line = '{}:{}:{}:{}:{}'.format(host, port, database, user, password)
    logging.debug(pg_line)
    with open(PGPASS_FILE, 'w') as pass_file:
        pass_file.write(pg_line)

    logging.debug('Chmod-ing the file to 600 as per postgres docs.')
    os.chmod(PGPASS_FILE, 0600)


def find_latest_dump(dump_dir, host, database):
    """
    returns the file path of the latest dump file from the same host and
    database.
    """
    files = [os.path.join(dump_dir, f) for f in os.listdir(dump_dir)
             if os.path.isfile(os.path.join(dump_dir, f)) and
                f.startswith('{}-{}'.format(host, database))]
    latest_file = max(files, key=os.path.getmtime)
    return os.path.abspath(latest_file)


def get_dump_filename(host, database):
    """
    forms a filename based on time host and DB name.
    """
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    file_name = '{}-{}-{}.pgdump'.format(host, database, now)
    backup_file_ = os.path.join(DUMP_DIR, file_name)
    logging.info('Formed backup filename: {}'.format(backup_file_))
    return backup_file_


def create_empty_local_db(dev_host, dev_port, dev_user, database):
    """
    locally create the database that you will be restoring to
    """
    cmd = '/usr/bin/createdb --host {h} -p {p} -U {u} {db}'.format(
        h=dev_host, p=dev_port, u=dev_user, db=database)
    local(cmd)


def restore_dump_to_dev(dev_host, dev_port, dev_user, database, dump_file):
    """
    restores the dump file to the dev postgres server
    """
    cmd = '/usr/bin/pg_restore --host {h} --port {p} --username ' \
          '"{u}" --dbname "{db}" --no-password  --verbose ' \
          '"{dump_file}"'.format(h=dev_host, p=dev_port, u=dev_user,
                                 db=database, dump_file=dump_file)
    local(cmd)


def upload_dump_to_ucp_hcp(file_to_upload, upload_url):
    logging.info('About to upload file: {}'.format(file_to_upload))
    local('curl -u ucpbackup:534hawks -k -T {} {}'.format(file_to_upload, upload_url))
    logging.info('Finished uploading file to {}.'.format(upload_url))


if __name__ == '__main__':
    args = parser.parse_args()

    if not args.host:
        if args.database in DB_MAP:
            args.host = DB_MAP[args.database]
        else:
            args.host = HOST

    if not os.path.isdir(args.dump_dir) and not args.local:
        os.mkdir(args.dump_dir)

    if args.command == 'backup':
        logging.info('Chose to backup {}'.format(args.host))
        latest_local_db_file = get_dump_filename(args.host, args.database)
        logging.info('Dump file: [{}]'.format(latest_local_db_file))
        pg_dump(args.host, args.port, args.user, args.database, latest_local_db_file)
        logging.info('Dumping DB finished.')
        logging.info('{}'.format(latest_local_db_file))

        upload_dump_to_ucp_hcp(latest_local_db_file, args.upload_url)

        sys.exit(0)

    if not args.local:
        create_pg_pass_file(args.host, args.port,
                            args.database, args.user, args.password)
        latest_local_db_file = get_dump_filename(args.host, args.database)
        logging.info('Dump file: [{}]'.format(latest_local_db_file))

        pg_dump(args.host, args.port, args.user, args.database,
                latest_local_db_file)
    else:
        if not os.path.isdir(args.dump_dir):
            logging.error('Using local but could not find dump dir: {}'.format(
                args.dump_dir))
            sys.exit(1)

        latest_local_db_file = find_latest_dump(args.dump_dir, args.host,
                                                args.database)
        logging.info('Found latest local dump: {}'.format(latest_local_db_file))

    delete_local_db(args.dev_host, args.dev_port, args.dev_user, args.database)

    create_empty_local_db(args.dev_host, args.dev_port, args.dev_user,
                          args.database)

    restore_dump_to_dev(args.dev_host, args.dev_port, args.dev_user,
                        args.database, latest_local_db_file)