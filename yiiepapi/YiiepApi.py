from yiiepapi.numerums import ApiClient
import yiiepapi.apiconfig as config

class YiiepApi(ApiClient):
    '''
    API client for Yiiep payment platform
    '''

    def __init__(self, testmode = config.TESTMODE, API_ID = config.API_ID, API_KEY = config.API_KEY):
        ''' Class Constructor '''
        super(YiiepApi, self).__init__(testmode, API_ID, API_KEY)

    ########## Webservices functions ##########
    def presetBill(self, billId, billAmount, billCurrency):
        '''
        Preset a bill on yiiep platform for payment
        param: billId : string - Your unique ID for the current bill
        param: billAmount : float - The total amount of the bill
        param: billCurrency : string - Currency ISO [XOF | XAF ]
        '''
        #Params
        params = {}
        params['bill'] = billId
        params['value'] = float(billAmount)
        params['crcy'] = billCurrency

        #Query
        return self.isSuccess(self.send('preset', params))

    def unsetBill(self, billHash):
        ''' 
        Unset a bill on yiiep platform
        param: billHash: string - Yiiep unique id returned by presetBill
        return: boolean
        '''
        params = {}
        params['hash'] = billHash

        #Query
        return self.isSuccess(self.send('unset', params))

    def payBill(self, billHash, paycode):
        '''
        Pay a bill previously preseted
        param: billHash: string - Yiiep unique id returned by presetBill
        param: paycode: string - Mobile money transfert code coresponding to payment
        '''
        #Params
        params = {}
        params['hash'] = billHash
        params['paycode'] = paycode
        
        return self.isSuccess(self.send('pay', params))
    
    def checkBill(self, billHash):
        '''
        Check a bill payment state
        param: billHash: string - Yiiep unique id returned by presetBill
        return: boolean
        JSON data contain : []
        '''
        #Params
        params = {}
        params['hash'] = billHash

        return self.isSuccess(self.send('bstate', params))

    def accountState(self):
        '''
        Check account your app account state
        return: boolean
        JSON data contain : [state, xofbalance, currency, balance]
        '''
        #Params
        params = {}
        #TODO : add param to handle date period

        return self.isSuccess(self.send('astate', params))

    def refundBill(self, billHash):
        '''
        Refund a bill previously paid
        param: billHash: string - Yiiep unique id returned by presetBill
        return: boolean
        JSON data contain : [hash, xofbalance, currency, balance]
        '''
        #Params
        params = {}
        params['hash'] = billHash

        return self.isSuccess(self.send('refund', params))

    ########## Utility functions ##########

    def payUrl(self, billhash):
        '''
        Generate a url string corresponding to yiiep payment link for specified bill
        param: billHash: string - Yiiep unique id returned by presetBill
        return string
        '''
        return "{}pay/{}".format(self.baseUrl, billhash)

    def qrSource(self, billhash):
        '''
        Generate a url string corresponding to yiiep payment QR Code for specified bill
        param: billHash: string - Yiiep unique id returned by presetBill
        return string
        '''
        return "{}qrcode/{}".format(self.baseUrl, billhash)

    def payLink(self, billhash, cssClass = ''):
        '''
        Generate an HTML tag for Yiiep payment link
        param: billHash: string - Yiiep unique id returned by presetBill
        param: cssClass: string - Provide a css class to format the link at your convenience
        '''
        payUrl = self.qrSource(billhash)
        return '<a class="{}" target="_blank" href="{}">YiiepPay</a>'.format(cssClass, payUrl)

    def payQR(self, billhash, cssClass = ''):
        '''
        Generate an HTML tag for Yiiep payment QR code
        param: billHash: string - Yiiep unique id returned by presetBill
        param: cssClass: string - Provide a css class to format the link at your convenience
        '''
        qrSrc = self.qrSource(billhash)
        return '<a target="_blank" href="{}pay/{}"><img src="{}" class="{}"></a>'.format(self.baseUrl, billhash, qrSrc, cssClass)

    

