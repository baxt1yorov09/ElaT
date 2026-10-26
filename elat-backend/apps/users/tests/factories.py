from __future__ import annotations

import factory

from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    phone = factory.Sequence(lambda n: f"+99890{n:07d}")
    name = factory.Sequence(lambda n: f"Test User {n}")
    is_verified = True
