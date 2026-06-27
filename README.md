# Notification Service

Notification Service stores user notifications and delivers them in real time over WebSockets. Other services call its internal APIs or the shared notification client to create notification records and fan them out through Redis-backed Django Channels.

## Responsibilities

- Persist notifications for platform users.
- List a user's notifications and unread count.
- Mark one or all user notifications as read.
- Create notifications from internal services.
- Broadcast notifications to multiple users through an internal endpoint.
- Deliver real-time events to authenticated WebSocket connections.

## Features

- Per-user notification feed.
- Read/unread state management.
- Internal notification creation and broadcast.
- WebSocket group delivery on `user_<user_id>`.
- Redis-backed channel layer.

## API Endpoints

Base path: `/api/`

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `GET` | `notifications/` | Bearer JWT | List notifications for the authenticated user. |
| `GET` | `notifications/unread-count/` | Bearer JWT | Return unread notification count. |
| `PATCH` | `notifications/<notification_id>/read/` | Bearer JWT | Mark one notification as read. |
| `PATCH` | `notifications/read-all/` | Bearer JWT | Mark all authenticated user's notifications as read. |

## Internal Service Endpoints

Internal endpoints use `X-Service-Key: <SERVICE_API_KEY>`.

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `internal/notifications/create/` | Create and deliver one notification. Expects `user_id`, `type`, `title`, `message`, optional `payload`. |
| `GET` | `internal/notifications/` | Return paginated notification summaries. |
| `GET` | `internal/notifications/<notification_id>/` | Return one notification summary. |
| `POST` | `internal/notifications/broadcast/` | Create notifications for supplied `user_ids`. |

## WebSocket API

| Path | Auth | Description |
| --- | --- | --- |
| `ws/notifications/?token=<JWT>` | Query-string JWT | Subscribe to notifications for the authenticated user. |

The consumer sends JSON containing `id`, `type`, `title`, `message`, `payload`, `is_read`, and `created_at`.

## Authentication

REST endpoints use `myapp.authentication.CustomJWTAuthentication`. WebSocket authentication is handled by `myapp.middleware.JWTAuthMiddleware`, which decodes the `token` query parameter with the shared RS256 public key.

## Environment Variables

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key. |
| `DEBUG` | Enables debug mode when set to `1`, `true`, or `yes`. |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts. Defaults to `*`. |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | MySQL database configuration. |
| `JWT_PUBLIC_KEY_PATH` | Public key used for REST and WebSocket JWT verification. |
| `SERVICE_API_KEY` | Shared key for internal endpoints. |
| `REDIS_HOST`, `REDIS_PORT` | Redis connection used by Channels. Defaults to `127.0.0.1:6379`. |
| `*_SERVICE_URL` | Optional service URL settings loaded by settings. |

## Setup

```bash
cd NotificationService_labora
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
daphne notificationservice.asgi:application -p 8010
```

Redis must be running for WebSocket delivery.

## Service Architecture

- Django project: `notificationservice`
- App: `myapp`
- REST views: `myapp/views.py`
- Notification fan-out helper: `myapp/services.py`
- WebSocket consumer: `myapp/consumers.py`
- Channel routing: `myapp/routing.py`
- Internal permission: `myapp.permissions.internal_service.IsInternalService`

## Database Models

- `Notification`: stores `user_id`, `notification_type`, `title`, `message`, JSON `payload`, read flag, and creation timestamp.

## Notification/Event Flow

`create_notification()` writes a notification row, builds a payload, and sends it through the Channels layer to group `user_<user_id>`. Connected WebSocket clients for that user receive the event immediately.
