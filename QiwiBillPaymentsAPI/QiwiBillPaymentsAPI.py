import json
import uuid
import urllib.parse
import requests
from time import gmtime, strftime
from datetime import datetime, timedelta

class QiwiBillPaymentsException(Exception):
    pass

class QiwiBillPaymentsAPI:
    API_URL = 'https://api.qiwi.com/partner/bill/v1/bills/'
    CLIENT_NAME = 'python_sdk'
    CLIENT_VERSION = '0.1'
    def __init__(self, public_key, secret_key):
        """
        Construct the object
        :param public_key: str public     key from p2p.qiwi.com
        :param secret_key: str secret     key from p2p.qiwi.com
        :return            <Response >    Return response with result
        """

        self.public_key = public_key
        self.secret_key = secret_key

        self.session = requests.Session()

    def __normalizeAmount(self, amount=0):
        """
        Normalize amount
        :param amount:    float | str   The amount
        :return:          float(.2)     Normalize result
        """
        return float('{:.2f}'.format(amount))

    def getLifetimeByDay(self, days=45):
        """
        Generate lifetime in format YYYY-mm-ddTcc:mm:ss+/-cc:mm
        :param days:    int    Days of lifetime
        :return:        str    Lifetime in ISO
        """
        date = datetime.now()
        timePlused = timedelta(days) + date

        tz_str = strftime('%z', gmtime())
        tz_str = tz_str[0:3] + ':' + tz_str[3:]

        return timePlused.strftime('%Y-%m-%dT%I:%M:%S') + tz_str

    def generateID(self):
        """
        Generate id
        :return:    str   Return uuid v4
        """
        return uuid.uuid4()

    def createPaymentForm(self, params):
        """
        Creating checkout link
        :param params:               dict        The parameters
        :param params.billID:        str | int   The bill identifier
        :param params.publicKey      str         The public key
        :param params.amount         str | int   The amount
        :param params.successUrl     str         The success url
        :return:                     str         Return checkout link
        """
        url = 'https://oplata.qiwi.com/create'
        amount = self.__normalizeAmount(params['amount'])
        params['amount'] = amount

        strParams = urllib.parse.urlencode(params)
        return url + '?' + strParams

    def createBill(self, billID, params):
        """
        Creating bill
        :param billID:                        str | int     The bill identifier
        :param params:                        dict          The parameters
        :param params.amount:                 str | int     The amount
        :param params.currency:               str           The currency
        :param [params.comment]:              str           The bill comment
        :param params.expirationDateTime:     str           The bill expiration datetime (ISO string)
        :param [params.customFields]:         dict          The bill custom fields
        :param params.phone:                  str           The phone
        :param params.email:                  str           The email
        :param params.account:                str           The account
        :param params.successUrl:             str           The success url
        :return:
        """
        params.customFields['apiClient'] = self.CLIENT_NAME
        params.customFields['apiClientVersion'] = self.CLIENT_VERSION

        body = {
            'amount': {
                'currency': params['currency'],
                'amount': params['amount']
            },
            'comment': params['comment'],
            'expirationDateTime': params['expirationDateTime'],
            'customer': {
                'phone': params['phone'],
                'email': params['email'],
                'account': params['account']
            },
            'customFields': params['customFields']
        }

        response = self.requestBuilder(billID, 'PUT', body=body)

        if response.status_code == 200:
            return json.loads(response.text)

        raise QiwiBillPaymentsException

    def getBillInfo(self, billID):
        response = self.requestBuilder(billID, 'GET')

        if response.status_code == 200:
            return json.loads(response.text)

        raise QiwiBillPaymentsException

    def cancelBill(self, billID):
        self.requestBuilder(billID + '/reject', 'POST')

    def getRefundInfo(self, billID, refundID):
        url = billID + '/refunds/' + refundID

        response = self.requestBuilder(url, 'GET')

        if response.status_code == 200:
            return json.loads(response.text)

        raise QiwiBillPaymentsException

    def refund(self, billID, refundID, amount=0, currency='RUB'):
        amount = self.__normalizeAmount(amount)

        url = billID + '/refunds/' + refundID

        body = {
            'amount': {
                'currency': currency,
                'value': amount
            }
        }

        response = self.requestBuilder(url, 'PUT', body)

        if response.status_code == 200:
            return json.loads(response.text)

        raise QiwiBillPaymentsException

    def requestBuilder(self, endpoint, method, body=None):
        """
        Build request
        :param endpoint:
        :param method:
        :param body:
        :return:
        """
        self.session.headers = {
            'Content-Type': 'application/json;charser=UTF-8',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.secret_key
        }

        if method == 'GET':
            return self.session.get(self.API_URL + endpoint)
        elif method == 'POST':
            return self.session.post(self.API_URL + endpoint, json.dumps(body))
        elif method == 'PUT':
            return self.session.put(self.API_URL + endpoint, json.dumps(body))
