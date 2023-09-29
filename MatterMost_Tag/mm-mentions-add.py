import sys
import argparse

from playhouse.postgres_ext import (
    PostgresqlExtDatabase,
    CharField,
    BigIntegerField,
    BooleanField,
    JSONField,
    IntegerField
)


host = 'DB_Host'
port = 'DB_Port'
user = 'DB_User'
password = 'DB_Password'
database = 'DB'

db = PostgresqlExtDatabase(database, user=user, password=password, host=host, port=port)


class User(db.Model):
    id = CharField(primary_key=True, max_length=26)
    createat = BigIntegerField()
    updateat = BigIntegerField()
    deleteat = BigIntegerField()
    username = CharField(max_length=64)
    password = CharField(max_length=128)
    authdata = CharField(max_length=128)
    authservice = CharField(max_length=32)
    email = CharField(max_length=128)
    emailverified = BooleanField()
    nickname = CharField(max_length=64)
    firstname = CharField(max_length=64)
    lastname = CharField(max_length=64)
    roles = CharField(max_length=256)
    allowmarketing = BooleanField()
    props = JSONField()
    notifyprops = JSONField()
    lastpasswordupdate = BigIntegerField()
    lastpictureupdate = BigIntegerField()
    failedattempts = IntegerField()
    locale = CharField(max_length=5)
    mfaactive = BooleanField()
    mfasecret = CharField(max_length=128)
    position = CharField(max_length=128)
    timezone = JSONField()
    remoteid = CharField(max_length=26)

    class Meta:
        database = db
        db_table = 'users'


QUERY_JSON = {
    'push': 'mention',
    'email': 'false',
    'channel': 'true',
    'desktop': 'mention',
    'comments': 'never',
    'first_name': 'false',
    'push_status': 'away',
    'mention_keys': '@TAG',
    'push_threads': 'all',
    'desktop_sound': 'true',
    'email_threads': 'all',
    'desktop_threads': 'all',
    'auto_responder_active': 'false',
    'auto_responder_message': 'Hello, I am out of office and unable to respond to messages.',
    'desktop_notification_sound': 'Bing'
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Updating Data in a Database')

    parser.add_argument(
        'mails',
        metavar='N',
        type=str,
        nargs='+',
        help='List of mails separated by spaces')

    parser.add_argument(
        '--tag',
        type=str,
        nargs='+',
        help='List of tags separated by commas')

    args = parser.parse_args()
    mails = args.mails
    tags = args.tag
    tags = ','.join(tags)

    if not mails or not tags:
        parser.print_help()
        sys.exit(2)

    db.connect()

    with db:
        for email in mails:
            user = User.get_or_none(User.email == email)

            if not user:
                print('No data found with this email!')
                sys.exit(2)


            QUERY_JSON['mention_keys'] = tags
            if user.notifyprops:
                if user.notifyprops['mention_keys']:
                    if tags not in user.notifyprops['mention_keys']:
                        user.notifyprops['mention_keys'] += ',' + tags
                else:
                    user.notifyprops['mention_keys'] = tags
            else:
                user.notifyprops = QUERY_JSON
            user.save()

            print(f'Record {email} updated')