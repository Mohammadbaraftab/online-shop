from kavenegar import *

def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('78793239306367616237736469765531666F537363506F33486153584A617651306D5376423038555778633D')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f"{code} کد تایید شما ",
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)