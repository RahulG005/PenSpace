import requests
import json

from . models import Subscription
from django.conf import settings

def get_access_token():
    data = {"grant_type": "client_credentials"}
    headers = {"Accept": "application/json","Accept-language": "en_US"}

    client_id = settings.SS_CLIENT_ID

    secret_id = settings.SS_SECRET_ID

    url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"

    r = requests.post(url,auth=(client_id, secret_id),headers=headers, data = data).json()

    access_token = r['access_token']
    print(access_token)

    return access_token

def cancel_subscription_paypal(access_token, subID):

    bearer_token = 'Bearer' + ' ' + access_token
    

    headers = {
        'content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    url = f'https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subID}/cancel'

    r = requests.post(url, headers = headers)

    print(r.status_code)
    print(bearer_token)


def update_subscription_paypal(access_token, subID):

    bearer_token = 'Bearer ' + ' ' +  access_token

    headers = {

        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    subDetails = Subscription.objects.get(paypal_subscription_id=subID)

    # Obtain the current subscription plan for the user/client (Standard / Premium)

    current_sub_plan = subDetails.subscription_plan

    if current_sub_plan == "Standard":

        new_sub_plan_id = 'P-3V393143PG1484408M2DTOLQ'  # To Premium

    elif current_sub_plan == "Premium":

        new_sub_plan_id = 'P-1L542628C1700650YM2DTNHI'# To Standard


    url = 'https://api.sandbox.paypal.com/v1/billing/subscriptions/' + subID + '/revise'

    print(new_sub_plan_id)

    revision_data = {

        "plan_id": new_sub_plan_id

    }

    # Make a POST request to PayPal's API for updating/revising a subscription

    r = requests.post(url, headers=headers, data=json.dumps(revision_data))



    # Output the response from PayPal

    response_data = r.json()

    print(response_data)


    approve_link = None

    for link in response_data.get('links', []):

        if link.get('rel') == 'approve':

            approve_link = link['href']


    if r.status_code == 200:

        print("Request was a success")

        return approve_link

    else:

        print("Sorry, an error occured!")


def get_current_subscription(access_token, subID):

    bearer_token = 'Bearer ' + ' '+ access_token

    headers = {

        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    url = f'https://api.sandbox.paypal.com/v1/billing/subscriptions/{subID}'

    r = requests.get(url, headers=headers)

    if r.status_code == 200:

        subscription_data = r.json()

        current_plan_id = subscription_data.get('plan_id')

        return current_plan_id

    else:

        print("Failed to retrieve subscription details")

        return None