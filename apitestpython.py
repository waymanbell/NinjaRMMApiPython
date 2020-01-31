import base64, hmac, hashlib, datetime, requests
from time import mktime
from wsgiref.handlers import format_date_time
from myauthcreds import access_key_id, secret_key


def getStringToSign(httpMethod, contentMD5, contentType, requestDate, canonicalPath):
    stringToSign =[]
    stringToSign.append(httpMethod + '\n')
    stringToSign.append((contentMD5 + '\n') if contentMD5 != None else '\n')
    stringToSign.append((contentType + '\n') if contentType != None else '\n')
    stringToSign.append(requestDate + '\n')
    stringToSign.append(canonicalPath)

    stringToSign = ''.join(stringToSign)

    return stringToSign

    
def getSignature(secret_key, string_to_sign):
    encoded_string = base64.b64encode(string_to_sign.encode('UTF-8')).decode('UTF-8').replace('\n','').replace('\r', '')
    encoded_string = encoded_string.encode('UTF-8')
    encoded_secret_key = hmac.new(secret_key.encode('UTF-8'), encoded_string, hashlib.sha1)
    signature = base64.b64encode(encoded_secret_key.digest()).decode('UTF-8')
    return signature


#Build http request
httpMethod = 'GET'
contentMD5 = ''
contentType = ''
requestDate = format_date_time(mktime(datetime.datetime.now().timetuple()))
canonicalPath = '/v1/customers'

stringToSign = getStringToSign(httpMethod, contentMD5, contentType, requestDate, canonicalPath)
signature = getSignature(secret_key, stringToSign)

#Send request and collect response
response = requests.get('http://api.ninjarmm.com/v1/customers', headers = {'Date' : requestDate, 'Authorization' : 'NJ ' + access_key_id + ':' + signature})

#Print reponse
print(response)
