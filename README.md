# NestDaddy for Dify

Give your Dify apps and agents today's internet: live web search and real-time news from NestDaddy's own search index.

**Source code:** https://github.com/nestdaddy/dify-nestdaddy

## Tools

| Tool | What it does |
|---|---|
| **NestDaddy Web Search** | Searches the web and returns the title, URL, snippet and domain of each page. Fresh news is mixed in for time-sensitive questions. |
| **NestDaddy News Search** | Searches real-time news from around the world, newest and best match first. Optional country (two-letter code) and time range (1-120 days). |

## Setup

1. Get a free API key at [nestdaddy.com](https://nestdaddy.com/dashboard). The Free plan includes 1,000 credits a month and needs no card. One search costs 1 credit.
2. In Dify, install the **NestDaddy** plugin from the Marketplace.
3. Open **Tools > NestDaddy > Authorize** and paste your API key.

## Usage

- **In an Agent:** add *NestDaddy Web Search* and *NestDaddy News Search* as tools. The model decides when to call them, for example for "What happened in AI news today?" or "Find the pricing page of Supabase".
- **In a Workflow:** add a tool node, choose a NestDaddy tool, and pass the query from an earlier node. Each tool returns a readable text answer and a JSON result (`results` with `title`, `url` and either `snippet` or `summary`) for later nodes.

## Requirements

- A NestDaddy API key (free plan available).
- Outbound HTTPS access from your Dify instance to `https://nestdaddy.com`. The plugin calls only the fixed endpoints `/api/v1/search` and `/api/v1/news/search`.

## Support

- Questions or problems: open an issue at https://github.com/nestdaddy/dify-nestdaddy/issues or email support@nestdaddy.com
- Community: https://discord.gg/CXStfSFC3v
- API docs: https://nestdaddy.com/apis

## Privacy

See [PRIVACY.md](PRIVACY.md).
