# Universal payments API Python SDK

Python SDK модуль для внедрения единого платежного протокола эквайринга и QIWI Кошелька.

## Установка и подключение
Установка с помощью pip:

```bash
pip3 install qiwiBillPaymentsAPI
```

Подключение:

```python
from QiwiBillPaymentsAPI import QiwiBillPaymentsAPI
```

## Документация

**API P2P-счетов (для физических лиц)**: https://developer.qiwi.com/ru/p2p-payments
**API QIWI Кассы (для юридических лиц)**: https://developer.qiwi.com/ru/bill-payments

## Авторизация

Для использования SDK требуется `PUBLIC_KEY` и `SECRET_KEY`, подробности в [документации](https://developer.qiwi.com/ru/bill-payments/#auth).

```python
PUBLIC_KEY = '48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iPywsuk1L1SFfXsQkJYBHTMPqBjvf57v4MCz22zbCf67Lz6fdJFmn2UuziWYc2aubucguB9R7yhBvnVjdHV6tTDKNQvcPEQEAV*********'
SECRET_KEY = 'eyJ2ZXJzaW9uIjoicmVzdF92MyIsImRhdGEiOnsibWVyY2hhbnRfaWQiOjUyNjgxMiwiYXBpX3VzZXJfaWQiOjcxNjI2MTk3LCJzZWNyZXQiOiJmZjBiZmJiM2UxYzc0MjY3YjIyZDIzOGYzMDBkNDhlYjhiNTnONPININONPN090MTg5Z**********************'

qiwiApi = QiwiBillPaymentsAPI(PUBLIC_KEY, SECRET_KEY)
```

Смена `PUBLIC_KEY` и `SECRET_KEY` на новый:

```python
NEW_PUBLIC_KEY = 'cmVzdF92MyIsImRhdGEiOnsibWVyY2hhbnRfaWQiOjUyNjgxMiwiYXBpX3VzZXJfaWQiOjcxNjI2MTk3LCJzZWNyZXQiOiJmZjBiZmJiM2UxYzc0MjY3YjIyZDIzOGYzMDBkNDhlYjhiNTk5NmIbhchhbbiNTk5NmIbhHBHIBDBI*****************'
NEW_SECRET_KEY = 'kokoOKPzaW9uIjoicmVzdF92MyIsImRhdGEiOnsibWVyY2hhbnRfaWQiOjUyNjgxMiwiYXBpX3VzZXJfaWQiOjcxNjI2MTk3LCJzZWNyZXQiOiJmZjBiZmJiM2UxYzc0MjY3YjIyZDIzOGYzMDBkNDhlYjhiNTk5NmIbhchhbbHBHIBDBI**********************'

qiwiApi.public_key = NEW_PUBLIC_KEY
qiwiApi.secret_key = NEW_SECRET_KEY
```

## Примеры

По-умолчанию пользователю доступно несколько способов оплаты. В платежной форме параметры счета передаются в открытом виде в ссылке. Далее клиенту отображается форма с выбором способа оплаты. При использовании этого способа нельзя гарантировать, что все счета выставлены мерчантом, в отличие от выставления по API.
Через API все параметры передаются в закрытом виде , так же в API поддерживаются операции выставления и отмены счетов, возврата средств по оплаченным счетам, а также проверки статуса выполнения операций.

### Платежная форма

Простой способ для интеграции. При открытии формы клиенту автоматически выставляется счет. Параметры счета передаются в открытом виде в ссылке. Далее клиенту отображается платежная форма с выбором способа оплаты. При использовании этого способа нельзя гарантировать, что все счета выставлены мерчантом, в отличие от выставления по API.

Метод `createPaymentForm` создает платежную форму. В параметрах нужно указать: ключ идентификации провайдера, полученный в QIWI Кассе `publicKey`, идентификатор счета `billId` внутри вашей системы и сумму `amount`. В результате будет получена ссылка на форму оплаты, которую можно передать клиенту. Подробнее о доступных параметрах в [документации](https://developer.qiwi.com/ru/bill-payments/#http).

```python
params = {
    'publicKey': qiwiApi.public_key,
    'amount': 200,
    'billId': '893794793973',
    'successUrl': 'https://merchant.com/payment/success?billId=893794793973'
}

link = qiwiApi.createPaymentForm(params)
```

В результате:

```
https://oplata.qiwi.com/create?publicKey=2tbp1WQvsgQeziGY9vTLe9vDZNg7tmCymb4Lh6STQokqKrpCC6qrUUKEDZAJ7mvFnzr1yTebUiQaBLDnebLMMxL8nc6FF5zfmGQnypdXCbQJqHEJW5RJmKfj8nvgc&amount=200&billId=893794793973&successUrl=https%3A%2F%2Fmerchant.com%2Fpayment%2Fsuccess%3FbillId%3D893794793973&customFields[apiClient]=node_sdk&customFields[apiClientVersion]=3.1.2
```

### Выставление счета

Надежный способ для интеграции. Параметры передаются server2server с использованием авторизации. Метод позволяет выставить счет, при успешном выполнении запроса в ответе вернется параметр `payUrl` - ссылка для редиректа пользователя на платежную форму.

Метод `createBill` выставляет новый счет. В параметрах нужно указать: идентификатор счета `billId` внутри вашей системы и дополнительными параметрами `fields`. В результате будет получен ответ с данными о выставленном счете.

```python
billId = 'cc961e8d-d4d6-4f02-b737-2297e51fb48e'

fields = {
    'amount': 1.00,
    'currency': 'RUB',
    'comment': 'test',
    'expirationDateTime': '2018-03-02T08:44:07',
    'email': 'example@mail.org',
    'account' : 'client4563',
    'successUrl': 'http://test.ru/'
}

bill = qiwiApi.createBill(billId, fields)
```

В результате:

```json
{
  "siteId": "270305",
  "billId": "cc961e8d-d4d6-4f02-b737-2297e51fb48e",
  "amount": {
    "currency": "RUB",
    "value": "200.34"
  },
  "status": {
    "value": "WAITING",
    "changedDateTime": "2018-07-12T10:28:38.855+03:00"
  },
  "comment": "test",
  "creationDateTime": "2018-07-12T10:28:38.855+03:00",
  "expirationDateTime": "2018-08-26T10:28:38.855+03:00",
  "payUrl": "https://oplata.qiwi.com/form/?invoice_uid=bb773791-9bd9-42c1-b8fc-3358cd108422&successUrl=http%3A%2F%2Ftest.ru%2F"
}
```

### Информация о счете

Метод `getBillInfo` возвращает информацию о счете. В параметрах нужно указать идентификатор счета `billId` внутри вашей системы, в результате будет получен ответ со статусом счета. Подробнее в [документации](https://developer.qiwi.com/ru/bill-payments/#invoice-status).

```python
billId = 'cc961e8d-d4d6-4f02-b737-2297e51fb48e';

billInfo = qiwiApi.getBillInfo(billId)
```

Ответ:

```json
{
  "siteId": "270305",
  "billId": "cc961e8d-d4d6-4f02-b737-2297e51fb48e",
  "amount": {
    "currency": "RUB",
    "value": "200.34"
  },
  "status": {
    "value": "WAITING",
    "changedDateTime": "2018-07-12T10:31:06.846+03:00"
  },
  "comment": "test",
  "creationDateTime": "2018-07-12T10:31:06.846+03:00",
  "expirationDateTime": "2018-08-26T10:31:06.846+03:00",
  "payUrl": "https://oplata.qiwi.com/form/?invoice_uid=ee3ad91d-cfb8-4dbf-8449-b6859fdfec3c"
}
```

### Отмена неоплаченного счета

Метод `cancelBill` отменяет неоплаченный счет. В параметрах нужно указать идентификатор счета `billId` внутри вашей системы, в результате будет получен ответ с информацией о счете. Подробнее в [документации](https://developer.qiwi.com/ru/bill-payments/#invoice-status).

```python
billId = 'cc961e8d-d4d6-4f02-b737-2297e51fb48e'

qiwiApi.cancelBill(billId)
```

Ответ:

```json
{
  "siteId": "270305",
  "billId": "cc961e8d-d4d6-4f02-b737-2297e51fb48e",
  "amount": {
    "currency": "RUB",
    "value": "200.34"
  },
  "status": {
    "value": "REJECTED",
    "changedDateTime": "2018-07-12T10:32:17.595+03:00"
  },
  "comment": "test",
  "creationDateTime": "2018-07-12T10:32:17.481+03:00",
  "expirationDateTime": "2018-08-26T10:32:17.481+03:00",
  "payUrl": "https://oplata.qiwi.com/form/?invoice_uid=cc961e8d-d4d6-4f02-b737-2297e51fb48e"
}
```

