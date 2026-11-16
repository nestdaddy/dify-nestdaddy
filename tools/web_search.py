from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._client import NestDaddyError, call, clamp

FIELDS = ("title", "url", "snippet", "domain", "type")


class NestDaddyWebSearchTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        query = str(tool_parameters.get("query") or "").strip()[:400]
        if not query:
            yield self.create_text_message("Please give some key words to search for.")
            return
        limit = clamp(tool_parameters.get("max_results"), 10, 1, 50)
        try:
            data = call(self.runtime.credentials.get("nestdaddy_api_key", ""), "/api/v1/search",
                        {"q": query, "limit": limit})
        except NestDaddyError as e:
            yield self.create_text_message(f"NestDaddy search failed: {e}")
            return
        results = [{k: r.get(k) for k in FIELDS if r.get(k) not in (None, "")}
                   for r in data.get("results") or [] if isinstance(r, dict)]
        yield self.create_json_message({"query": query, "count": len(results), "results": results})
        if not results:
            yield self.create_text_message(f'No web results for "{query}". Try fewer or different key words.')
            return
        lines = [f'Web results for "{query}":', ""]
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. {r.get('title') or r.get('url')}\n   {r.get('url')}")
            if r.get("snippet"):
                lines.append(f"   {r['snippet']}")
        yield self.create_text_message("\n".join(lines))
