import os
from functools import lru_cache
from urllib.parse import parse_qs

import jwt
from django.contrib.auth.models import AnonymousUser


MESSAGE_APP_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


@lru_cache(maxsize=1)
def _get_public_key_pem():

    path = os.environ.get(
        "JWT_PUBLIC_KEY_PATH",
        os.path.join(
            MESSAGE_APP_ROOT,
            "jwt_keys",
            "public.pem"
        )
    )

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class JWTAuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):

        scope["user"] = AnonymousUser()
        scope["user_id"] = None
        scope["role"] = None

        try:

            query_string = scope.get(
                "query_string",
                b""
            ).decode()
            query_params = parse_qs(query_string)

            token = query_params.get("token")

            if not token:

                return await self.app(
                    scope,
                    receive,
                    send
                )

            public_key = _get_public_key_pem()

            payload = jwt.decode(
                token[0],
                public_key,
                algorithms=["RS256"],
                options={
                    "verify_aud": False
                }
            )

            user_id = payload.get("user_id")
            role = payload.get("role")

            scope["user_id"] = user_id
            scope["role"] = role

        except jwt.ExpiredSignatureError:
            pass

        except jwt.InvalidTokenError:
            pass

        except FileNotFoundError:
            pass

        except Exception:
            pass

        return await self.app(
            scope,
            receive,
            send
        )
