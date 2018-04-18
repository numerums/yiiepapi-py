from yiiepapi import YiiepApi

yiiepApi = YiiepApi()

#fake bill
billID = 'PYTEST0001' #Change this
billAmount = 200
billCurrency = 'XOF'

##Preset Test
preset = yiiepApi.presetBill(billID, billAmount, billCurrency)

if(preset == True):
    print('Preset test succeed')
    #Get JSON data
    data = yiiepApi.data()
    print('Returned data : ')
    print(data)

    print("")

    #Get payment link
    print('Payment URL : ')
    paymentURL = yiiepApi.payUrl(data['billhash'])
    print(paymentURL)

    print("")

    #Get payment QRCODE link
    print('Payment QR Code URL : ')
    qrSource = yiiepApi.qrSource(data['billhash'])
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