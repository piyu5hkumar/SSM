
from re import T
from typing import Tuple
from django.core import validators
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import math
import datetime


class Otp(models.Model):
    class Otp_types(models.TextChoices):
        '''
        It extends TextChoices, this works for character like fields.
        Here each class variable will act as a choice and has type enum.

        For integer there is models.IntegerChoices and likewise for other type of model fields(check docs).

        Each class variable is of type enum, where the first value is the actual value to be set on the model, 
        and the second value is the human readable label name(It has nothing to do with the DB)

        1. To get all the choices just use Otp_types.choices and it will return a list of tuples of all the class variables

        2. To get the first value just use Otp_types.PHONE_VERIFICATION and to get the second value of an enum
        use Otp_types.PHONE_VERIFICATION.label
        '''

        # Don't get confuse, RHS are nothing but tuples
        TWO_FACTOR = 'two_factor', 'Two Factor Authentication'
        PHONE_VERIFICATION = 'phone_verification', 'Phone Number Verification'
        FORGOT_PASSWORD = "forgot_password", "Forgot Password"
        PAYMENT = "payment", "Payment Authentication"

    phone_number = models.CharField(validators=[MinLengthValidator(10)], max_length=10)
    otp_sent = models.CharField(max_length=4, validators=[MinLengthValidator(4)])
    date_created = models.DateTimeField(default=timezone.now)
    date_blocked = models.DateTimeField(null=True, blank=True)

    attempts = models.PositiveIntegerField(default=0)
    otp_type = models.CharField(max_length=255, choices=Otp_types.choices)
    is_used = models.BooleanField(default=False)
    is_latest = models.BooleanField(default=True)

    def is_blocked_and_cool_down_time(self):
        if not self.date_blocked:
            return False, None

        now = timezone.now()
        unblock_time = self.date_blocked + timezone.timedelta(seconds=settings.OTP_COOL_DOWN_TIME_SECONDS)

        if unblock_time < now:
            return False, None
        else:
            unblock_time_remaining = unblock_time - now

            unblock_time_hour, unblock_time_minute, unblock_time_second = (
                math.ceil(float(dt)) for dt in str(unblock_time_remaining).split(':')
            )

            unblock_time_remaining_datetime_time = datetime.time(
                unblock_time_hour, unblock_time_minute, unblock_time_second
            )

            return True, unblock_time_remaining_datetime_time

    @classmethod
    def is_applicable_for_otp(cls, phone_number, otp_type):
        """

        In this method we'll check the latest otp with the passed phone_number and otp_type,
        we will see whether it is blocked or not.
        -> If it is blocked then we'll return a tuple of
        False and a string containing the amount of time left for cool down
        -> If it is not blocked then we'll simply return a tuple of True and a string(which is not applicable tbh)

        """

        is_applicable = None
        message = None

        # Fetching latest otp with the passed phone_number and otp_type
        otp_qs = cls.objects.filter(phone_number=phone_number, otp_type=otp_type, is_latest=True)
        latest_otp = otp_qs.first()
        if latest_otp:
            is_blocked, cool_down_time = latest_otp.is_blocked_and_cool_down_time()

            if is_blocked:
                is_applicable = False
                message = "Max OTP limit({}) has reached, please wait for {} minute(s) and {} second(s)".format(
                    settings.OTP_FAILURE_ATTEMPTS,
                    cool_down_time.minute,
                    cool_down_time.second,
                )
                return is_applicable, message

        is_applicable = True
        message = "This user is applicable to send a new OTP"
        return is_applicable, message

    def is_expired(self):
        now = timezone.now()
        expiring_time = self.date_created + timezone.timedelta(
            seconds=settings.OTP_EXPIRE_SECONDS
        )
        if expiring_time <= now:
            return True
        else:
            return False

    @classmethod
    def validate_otp(cls, phone_number, otp_received, otp_type):
        is_validated = None
        message = None

        # Fetching all the Otp same as passed phone_number, otp_received and otp_type
        otp_qs = cls.objects.filter(
            phone_number=phone_number, otp_sent=otp_received, otp_type=otp_type
        )
        # If any/some record exists
        if otp_qs.exists():

            # We will check for the is_latest, because we don't want old otp to be able to validate
            otp_latest_qs = otp_qs.filter(is_latest=True)

            # If any/some record exists
            if otp_latest_qs.exists():
                otp_latest = otp_latest_qs.first()

                # Now we will see whether the latest otp has been used or not, if it is used
                if otp_latest.is_used:
                    is_validated = False
                    message = "This OTP was already used"

                # If the latest otp has not been used till yet
                else:

                    # If not used, lets check its expiration
                    if otp_latest.is_expired():
                        is_validated = False
                        message = "This OTP has been expired, please generate a new one"

                    # If not expired, then only we'll validate this otp
                    else:
                        otp_latest.is_used = True
                        otp_latest.save(updated_fields=["is_used"])
                        is_validated = True
                        message = "OTP validated successfully"
            else:
                is_validated = False
                message = "Please enter recently generated OTP"

        else:
            is_validated = False
            message = "Please enter valid OTP"

        return is_validated, message

    def already_cool_down_passed(self):
        '''

        This method will tell, whether after a sent OTP, do we need cool down time,
        but if already the cool down time elapsed after sending the otp, then no need for cool down,
        even though it might be 3rd otp of a type.
        If the time_delta > cool down time, then the new attempt will be the 1st attempt. 

        '''
        now = timezone.now()
        time_delta = now - self.date_created
        if time_delta > timezone.timedelta(seconds=settings.OTP_COOL_DOWN_TIME_SECONDS):
            return True
        else:
            return False

################################################## signals ##################################################


@receiver(pre_save, sender=Otp)
def increasing_attempts(sender, instance, *args, **kwargs):
    """

    We will fetch the latest otp object having same otp type and phone number, by so we'll update the
    current otp object's attempt number

    """

    # We don't want it to be called while an Otp object updates
    if kwargs["update_fields"]:
        return

    # Fetching latest otp having phone_number and otp_type same as the instance
    otp_qs = Otp.objects.filter(
        phone_number=instance.phone_number, otp_type=instance.otp_type, is_latest=True
    )
    latest_otp = otp_qs.first()

    if latest_otp:
        latest_otp.is_latest = False
        latest_otp.save(update_fields=["is_latest"])

        if latest_otp.is_used or latest_otp.already_cool_down_passed():
            '''
            If the latest otp was already used or enough time has passed then we'll assing the attempts of
            new otp to be 1. 
            '''
            instance.attempts = 1
        else:
            instance.attempts = latest_otp.attempts + 1
            """
            It is really important to understand here, that:
            -> When the attempts are exactly equal to the settings.OTP_FAILURE_ATTEMPTS,
            this means that this is the 3rd(in this case) consecutive otp of the same type and we have to date_block now, so that we don't receive any
            otp until cool down.
            -> When the attempts are exactly one more than settings.OTP_FAILURE_ATTEMPTS,
            this means that definitely we must have called the classmethod is_applicable_for_otp() before initializing the passed instance,
            that implies that during the 3rd(in this case) otp, definitely there would be a date_block, but now it must be cooled down that is why
            is_applicable_for_otp() passed and this instance is made. So, we have to again set the attempts to 1.
            """
            if instance.attempts == settings.OTP_FAILURE_ATTEMPTS:
                instance.date_blocked = timezone.now()
            elif instance.attempts == settings.OTP_FAILURE_ATTEMPTS + 1:
                instance.attempts = 1
    else:
        instance.attempts = 1
