import hashlib
import os
import re
import sqlite3
import uuid

from datetime import datetime

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

from django.conf import settings


REVERSE_LOOKUP_DB_PATH = os.path.join(settings.KOLIBRI_HOME, "phonehashreverselookup.db")
SALT_FILE_PATH = os.path.join(settings.KOLIBRI_HOME, "phonehashsalt.txt")


class ReverseLookupCursor(object):

    def __enter__(self):

        self.conn = sqlite3.connect(REVERSE_LOOKUP_DB_PATH)

        self.conn.execute("CREATE TABLE IF NOT EXISTS lookup (phone char PRIMARY KEY, hashval char NOT NULL, lastreward timestamp)")
        self.conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS hashval_index ON lookup (hashval)")

        self.cursor = self.conn.cursor()

        return self.cursor

    def __exit__(self, *args, **kwargs):

        self.cursor.close()
        self.conn.close()


def normalize_phone_number(phone):
    """Remove everything except digits from the phone number string."""
    return re.sub("\D", "", str(phone))


@lru_cache(maxsize=5000)
def get_hash_value(phone):
    """Calculate the hashed + salted value for a phone number, or retrieve from DB if it already exists."""
    
    # ensure phone number is in the form of a string
    phone = str(phone)
    
    # if value is already a hash for some reason, return it directly
    if re.match("^[\da-f]{30}$", phone):
        return phone

    # normalize the phone number to only digits
    phone = normalize_phone_number(phone)

    # try looking up the mapping in the reverse lookup DB, else calculate and insert
    with ReverseLookupCursor() as c:
        c.execute("SELECT hashval FROM lookup WHERE phone = ?", (phone,))
        result = c.fetchone()
        if result:
            hashval = result[0]
        else:
            hashval = hashlib.sha256(phone + get_salt()).hexdigest()[:30]
            c.execute("INSERT OR REPLACE INTO lookup (phone, hashval) VALUES (?, ?)", (phone, hashval))
            c.connection.commit()
        return hashval


@lru_cache(maxsize=5000)
def get_phone_number(hashval):
    """Look up the phone number for a specific hashval, from the reverse lookup database."""
    with ReverseLookupCursor() as c:
        c.execute("SELECT phone FROM lookup WHERE hashval = ?", (hashval,))
        result = c.fetchone()
        if result:
            return result[0]
        else:
            # if the phone number was not found, just return the original hashval
            return hashval


@lru_cache(maxsize=1)
def get_salt():
    """Retrieve this installation's salt value from disk, or generate it if it doesn't yet exist."""
    try:
        with open(SALT_FILE_PATH) as f:
            salt = f.read().strip()
    except:
        salt = uuid.uuid4().hex
        with open(SALT_FILE_PATH, "w") as f:
            f.write(salt)
    return salt
