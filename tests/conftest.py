import os
import pytest
import ssl

from dotenv import load_dotenv, find_dotenv
from pytest_bugzilla_notifier.bugzilla_rest_client import BugzillaRESTClient


# Hack because of how SSL certificates are verified by default in Python
'''
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context
'''

# Check to see if we have a dotenv file and use it
if find_dotenv():
    load_dotenv(find_dotenv())


@pytest.fixture(scope="module")
def bugzilla_secure_user_one():
    api_details = {
        'bugzilla_host': os.getenv('BUGZILLA_HOST'),
        'bugzilla_api_key': os.getenv('BUGZILLA_API_KEY_1')
    }
    client = BugzillaRESTClient(api_details)
    return client

