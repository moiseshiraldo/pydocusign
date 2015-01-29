#!/usr/bin/env python
# coding=utf-8
"""Sample script that demonstrates `pydocusign` usage for managing accounts.

See also http://iodocs.docusign.com/#tabEndpoint6

"""
import os

import pydocusign


def prompt(environ_key, description, default):
    try:
        return os.environ[environ_key]
    except KeyError:
        value = raw_input('{description} (default: "{default}"): '.format(
            default=default, description=description))
        if not value:
            return default
        else:
            return value


# Get configuration from environment or prompt the user...
root_url = prompt(
    'PYDOCUSIGN_ROOT_URL',
    'DocuSign API URL',
    'https://demo.docusign.net/restapi/v2')
username = prompt(
    'PYDOCUSIGN_USERNAME',
    'DocuSign API username',
    '')
password = prompt(
    'PYDOCUSIGN_PASSWORD',
    'DocuSign API password',
    '')
integrator_key = prompt(
    'PYDOCUSIGN_INTEGRATOR_KEY',
    'DocuSign API integrator key',
    '')
distributor_code = prompt(
    'PYDOCUSIGN_TEST_DISTRIBUTOR_CODE',
    'DocuSign API distributor code',
    '')
distributor_password = prompt(
    'PYDOCUSIGN_TEST_DISTRIBUTOR_PASSWORD',
    'DocuSign API distributor password',
    '')
callback_url = prompt(
    'PYDOCUSIGN_TEST_CALLBACK_URL',
    'Envelope callback URL',
    '')
signer_return_url = prompt(
    'PYDOCUSIGN_TEST_SIGNER_RETURN_URL',
    'Signer return URL',
    '')


# Create a client.
client = pydocusign.DocuSignClient(
    root_url=root_url,
    username=username,
    password=password,
    integrator_key=integrator_key,
)


# Login. Updates API URLs in client.
print("1. GET /login_information")
login_information = client.login_information()
print("   Received data: {data}".format(data=login_information))


# Get main account information.
print("2. GET /accounts/{accountId}".format(accountId=client.account_id))
account_information = client.get_account_information(client.account_id)
print("   Received data: {data}".format(data=account_information))


# Create a subsidiary account.
print("3. POST /accounts")
account_email = "benoit.bryon+pydocusign-test@novapost.fr"
account_password = "notasecret"
account_input = {
    "accountName": "Pydocusign Test Account",
    "accountSettings": [],
    "addressInformation": {
        "address1": "32 rue de Paradis",
        "address2": "",
        "city": "Paris",
        "country": "France",
        "fax": "",
        "phone": "",
        "postalCode": "75010",
        "state": "",
    },
    "creditCardInformation": None,
    "distributorCode": distributor_code,
    "distributorPassword": distributor_password,
    "initialUser": {
        "email": account_email,
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "Jean",
        "password": account_password,
        "suffixName": "",
        "title": "M",
        "userName": account_email,
        "userSettings": [],
    },
    "planInformation": {
        "planId": "64c9f146-91d8-4137-8367-fd3f3a23ef76",
    },
    "referralInformation": None,
    "socialAccountInformation": None,
}
account_data = client.post_account(account_input)
print("   Received data: {data}".format(data=account_data))

raw_input("Please activate account {} and type RET".format(account_email))

# Get subsidiary account information.
print("4. GET /accounts/{accountId}".format(
    accountId=account_data['accountId']))
account_information = client.get_account_information(client.account_id)
print("   Received data: {data}".format(data=account_information))


# In order to delete subsidiary account, we have to log in with this account.
subsidiary_client = pydocusign.DocuSignClient(
    root_url=root_url,
    username=account_data['userId'],
    password=account_password,
    integrator_key=integrator_key,  # Use the same key as main account!
)

# Login. Updates API URLs in client.
print("5. LOGIN WITH SUBSIDIARY ACCOUNT")
account_login_information = subsidiary_client.login_information()
print("   Received data: {data}".format(data=account_login_information))


# Delete subsidiary account.
print("6. DELETE /accounts/{accountId}".format(
    accountId=subsidiary_client.account_id))
deleted = subsidiary_client.delete_account(subsidiary_client.account_id)
print("   Received data: {data}".format(data=deleted))
