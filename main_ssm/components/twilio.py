# django imports
from django.conf import settings

# twilio imports
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# additional imports
from ..models import Otp
import os
import random


INVITATION_MESSAGE = '''{user_info} invited you to EL-Wallet.
It's a fast, simple and secure app we can use to sharing files over the internet.
Get it at

Play Store : {} 
App Store: {}'''

PLAY_STORE_LINK = 'this_is_a_play_store_link.com'
APP_STORE_LINK = 'this_is_a_app_store_link.com'

OTP_MESSAGE = '''Your OTP for {otp_type_label},
is {otp_code}.
Please sharing this to anyone else.

Thankyou.
'''


class Twilio:
    TWILIO_USE = settings.TWILIO_USE
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '')
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')

    def __init__(self) -> None:
        '''
        This is the constructor for Twilio class.
        In future a logger will also be initialized here.
        '''

        if self.TWILIO_USE:
            self.twilio_client = Client(
                self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)

    @classmethod
    def get_otp(cls, length=4):
        '''

        A method to generate random otp based on the length passes

        '''

        # if length is 1 then 0 is also in range and 10**0 is 1
        random_range_start = 10 ** (length - 1) if length > 1 else 0
        random_range_end = (10 ** length) - 1 if length >= 1 else 0

        otp = str(random.randint(random_range_start, random_range_end))
        return otp

    def send_otp(self, phone_number, otp_type, length):
        '''

        Method to send an otp to the passed phone_number and the otp_type.
        We are assuming all numbers are Indian

        '''

        is_applicable, message = Otp.is_applicable_for_otp(phone_number, otp_type)

        if is_applicable:
            otp_code = self.get_otp(length)
            otp_message = OTP_MESSAGE.format(otp_type_label=otp_type.label, otp_code=otp_code)

            try:
                # If TWILIO_USE is set to True in the settings.py file, only then twilio will work
                if self.TWILIO_USE:
                    twilio_response = self.twilio_client.messages.create(
                        body=otp_message,
                        from_=self.TWILIO_PHONE_NUMBER,
                        to=f'+91{phone_number}'
                    )
                Otp.objects.create(
                    phone_number=phone_number,
                    otp_sent=otp_code,
                    otp_type=otp_type
                )

                return True, f'Otp {otp_code}, has been sent to {phone_number}'

            except TwilioRestException as tre:
                error_code = str(tre.code)
                message = self.get_twilio_error_message(error_code)
                return False, message

            except Exception as e:
                message = str(e)
                return False, message
        else:
            return False, message

    @classmethod
    def get_twilio_error_message(cls, error_code):
        messages = {
            '60000': 'You have exceeded the maximum number of attempts to verify your phone number. Contact support please',
            '60002': 'Your phone number or country code is invalid',
            '60003': 'You have exceeded the maximum number of attempts to verify your phone number. Contact support please',
            '60004': 'Your phone number or country code is invalid',
            '60005': 'Your phone number or country code is invalid',
            '60022': 'The verification code you entered is incorrect',
            '60023': 'We could not find a pending verification for this phone number. Click on verify phone number again',
            '60033': 'Your phone number or country code is invalid',
            '60078': 'The country code associated with your phone number is invalid',
            '60082': 'We cannot send you the verification code to a phone that cannot receive text messages',
            '60083': 'The phone number you entered is not available to send you the verification code',
            '60202': 'Max check attempts reached',
            '60203': 'Max send attempts reached.',
            '60205': 'SMS is not supported by landline phone number',
            '60207': 'Max rate limits per service reached',
            '60600': 'None provisioned or Out of Coverage',
            '21421': 'PhoneNumber is invalid',
            '21422': 'PhoneNumber is not available',
            '21214': '\'To\' phone number cannot be reached',
            '21217': 'Phone number does not appear to be valid',
            '21401': 'Invalid Phone Number',
            '21407': 'This Phone Number type does not support SMS',
            '21451': 'Invalid area code',
            '21601': 'Phone number is not a valid SMS-capable inbound phone number',
            '21612': 'The \'To\' phone number is not currently reachable via SMS',
            '21614': '\'To\' number is not a valid mobile number',
            '21408': 'Permission to send an SMS has not been enabled for the region indicated by the \'To\' number',
            '21211': 'Invalid \'To\' Phone Number',
        }
        return messages.get(error_code, None) or messages['60000']
