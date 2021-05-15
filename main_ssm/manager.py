from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("phone_number is required to create this user")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extrafields):
        extrafields.setdefault("is_active", True)
        extrafields.setdefault("is_staff", True)
        extrafields.setdefault("is_superuser", True)

        if not extrafields.get("is_staff"):
            raise ValueError("is_staff must be True for a superuser")
        if not extrafields.get("is_superuser"):
            raise ValueError("is_superuser must be True for a superuser")

        return self.create_user(phone_number, password, **extrafields)
