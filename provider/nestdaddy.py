from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools._client import NestDaddyError, call


class NestDaddyProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            call(credentials.get("nestdaddy_api_key", ""), "/api/v1/search", {"q": "python", "limit": 1})
        except NestDaddyError as e:
            raise ToolProviderCredentialValidationError(str(e)) from e
