# yiiepapi-php
Yiiep payment plateform API for Python

Yiiep est une plateforme de payement en ligne basée sur le mobile money. Cet API vous permet d'intégrer Yiiep dans votre site web comme solution de payement. L'api génére un qrcode que votre client peut scanner avec [l'appication mobile Yiiep](https://play.google.com/store/apps/details?id=com.numerumservices.yiiep) pour initier le payement.

Visitez [www.yiiep.com](https://www.yiiep.com/) pour en savoir plus.

## Installation
1. Cloner / Télécharger et déconpresser le répertoire yiiepapi-py dans votre projet.
2. Installer les dépendances

```sh

cd yiiepapi-py
python setup.py install

```

## Obtenir un ID d'api pour votre site ou application
1. [Créer un compte](https://www.yiiep.com/login)
2. Enregistrez un site marchand

## Utilisation
Ci dessous un exemple d'utilisation de l'API. Une version fonctionnelle de cet exemple est disponible dans le dossier  [example](../../example).  Pour plus d'information veuillez consulter la documentation.

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
