# Authentication and Permissions Setup

## Token Authentication
- Enabled using `rest_framework.authtoken`.
- Users obtain tokens via `/api/get-token/`.
- Tokens must be included in the `Authorization` header:
  `Authorization: Token <token>`

## Permissions
- Default permission: `IsAuthenticated`
- BookViewSet requires authentication for all write operations.
- Unauthenticated users receive `401 Unauthorized`.
