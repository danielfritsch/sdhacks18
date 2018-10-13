from __future__ import absolute_import, print_function
from pprint import pprint
import unittest
import webbrowser
import requests

import docusign_esign as docusign
from docusign_esign import AuthenticationApi, TemplatesApi, EnvelopesApi
from docusign_esign.rest import ApiException

user_name = "a96e9681-bdf2-455b-ac7f-fd31102b9943"
integrator_key = "7b8be35e-8e27-4d2c-9b5d-b665cdcc88dc"
base_url = "https://demo.docusign.net/restapi"
oauth_base_url = "account-d.docusign.com" # use account.docusign.com for Live/Production
redirect_uri = "https://www.docusign.com/api"
private_key_filename = "keys/docusign_private_key.txt"
user_id = "301839c9-416b-48ce-aa72-d1d26598cdaf"
template_id = "97d0cf02-fab1-497c-a89c-aad8f8df2b46"

api_client = docusign.ApiClient(base_url)

# IMPORTANT NOTE:
# the first time you ask for a JWT access token, you should grant access by making the following call
# get DocuSign OAuth authorization url:
oauth_login_url = api_client.get_jwt_uri(integrator_key, redirect_uri, oauth_base_url)
# open DocuSign OAuth authorization url in the browser, login and grant access
# webbrowser.open_new_tab(oauth_login_url)
print('OAuth login URL: ' + oauth_login_url)

# END OF NOTE

URL = "https://account-d.docusign.com/oauth/auth?"
PARAMS = {'response_type': 'code', 'scope':'signature', 'client_id':'7b8be35e-8e27-4d2c-9b5d-b665cdcc88dc', 'state':'a39fh23hnf23', 'redirect_url':'http://danielfritsch.com'}
r = requests.get(url = URL, params = PARAMS)
print(r.text)

# configure the ApiClient to asynchronously get an access token and store it
api_client.configure_jwt_authorization_flow(private_key_filename, oauth_base_url, integrator_key, user_id, 3600)

docusign.configuration.api_client = api_client

template_role_name = 'ThisIsRole'

# create an envelope to be signed
envelope_definition = docusign.EnvelopeDefinition()
envelope_definition.email_subject = 'Please DocuSign: signed_work_contract.pdf'
envelope_definition.email_blurb = 'plz sign'

# assign template information including ID and role(s)
envelope_definition.template_id = template_id

# create a template role with a valid template_id and role_name and assign signer info
t_role = docusign.TemplateRole()
t_role.role_name = template_role_name
t_role.name ='John Doe'
t_role.email = user_name

# create a list of template roles and add our newly created role
# assign template role(s) to the envelope
envelope_definition.template_roles = [t_role]

# send the envelope by setting |status| to "sent". To save as a draft set to "created"
envelope_definition.status = 'sent'

auth_api = AuthenticationApi()
envelopes_api = EnvelopesApi()

try:
    login_info = auth_api.login(api_password='true', include_account_id_guid='true')
    assert login_info is not None
    assert len(login_info.login_accounts) > 0
    login_accounts = login_info.login_accounts
    assert login_accounts[0].account_id is not None

    base_url, _ = login_accounts[0].base_url.split('/v2')
    api_client.host = base_url
    docusign.configuration.api_client = api_client

    envelope_summary = envelopes_api.create_envelope(login_accounts[0].account_id, envelope_definition=envelope_definition)
    assert envelope_summary is not None
    assert envelope_summary.envelope_id is not None
    assert envelope_summary.status == 'sent'

    print("EnvelopeSummary: ", end="")
    pprint(envelope_summary)

except ApiException as e:
    print("\nException when calling DocuSign API: %s" % e)
    assert e is None # make the test case fail in case of an API exception
