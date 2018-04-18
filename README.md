# yiiepapi-py
Python API for Yiiep payment platform


```python
'''Please first edit apiconfig.py to set your app API id an key'''

from yiiepapi import YiiepApi

yiiepApi = YiiepApi()

#fake bill -- Change at your convenance
billID = 'PYTEST0001' #Change this
billAmount = 200
billCurrency = 'XOF'

##Preset Test
preset = yiiepApi.presetBill(billID, billAmount, billCurrency)

if(preset == True):
    print('Preset test succeed')
    #Get JSON data
    presetdata = yiiepApi.data()
    print('Returned data : ')
    print(presetdata)

    print("")

    #Get payment link
    print('Payment URL : ')
    paymentURL = yiiepApi.payUrl(presetdata['billhash'])
    print(paymentURL)

    print("")

    #Get payment QRCODE link
    print('Payment QR Code URL : ')
    qrSource = yiiepApi.qrSource(presetdata['billhash'])
    print(qrSource)

    #Do payment after user send monney to yiiep platform
    paid = yiiepApi.payBill(data['billhash'], 'AFAKECODE') #Payment will fail because paycode is fake
    if(paid == True):
        print('Bill paid')
        paymentdata = yiiepApi.data()
        print('Returned data : ')
        print(paymentdata)
    else:
        print('Payment faild')
        print(yiiepApi.message())
else:
    print('Preset test faild')
    print(yiiepApi.message())

```
