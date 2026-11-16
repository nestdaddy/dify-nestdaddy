import re
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._client import NestDaddyError, call, clamp

FIELDS = ("title", "url", "source_domain", "published_timestamp", "summary", "description", "country")


class NestDaddyNewsSearchTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        query = str(tool_parameters.get("query") or "").strip()[:400]
        if not query:
            yield self.create_text_message("Please give some key words to search the news for.")
            return
        country = str(tool_parameters.get("country") or "").strip().upper()
        if country and not re.fullmatch(r"[A-Z]{2}", country):
            country = ""   # ignore anything that is not a two-letter code
        params = {"q": query, "country": country or None,
                  "days": clamp(tool_parameters.get("days"), 30, 1, 120),
                  "limit": clamp(tool_parameters.get("max_results"), 10, 1, 50)}
        try:
            data = call(self.runtime.credentials.get("nestdaddy_api_key", ""), "/api/v1/news/search", params)
        except NestDaddyError as e:
            yield self.create_text_message(f"NestDaddy news search failed: {e}")
            return
        results = [{k: r.get(k) for k in FIELDS if r.get(k) not in (None, "")}
                   for r in data.get("results") or [] if isinstance(r, dict)]
        yield self.create_json_message({"query": query, "count": len(results), "results": results})
        if not results:
            yield self.create_text_message(f'No news for "{query}" in the last {params["days"]} days. '
                                           "Try other key words or a longer time range.")
            return
        lines = [f'News for "{query}":', ""]
        for i, r in enumerate(results, 1):
            meta = " · ".join(str(x) for x in (r.get("source_domain"), r.get("published_timestamp")) if x)
            lines.append(f"{i}. {r.get('title')}\n   {r.get('url')}" + (f"\n   {meta}" if meta else ""))
            text = r.get("summary") or r.get("description")
            if text:
                lines.append(f"   {str(text)[:300]}")
        yield self.create_text_message("\n".join(lines))
