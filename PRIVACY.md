# Privacy Policy

## What the plugin sends

When a tool runs, the plugin sends the search query and the tool options (country, number of days, number of results) to the NestDaddy API at `https://nestdaddy.com` over HTTPS, together with your API key. Nothing else from your Dify app, conversation or files is sent.

## What the plugin stores

The plugin itself stores nothing. It keeps no logs, caches or copies of queries or results.

## What NestDaddy does with the request

NestDaddy uses the request to return results and to count usage against your plan. Its handling of API requests is described in the NestDaddy privacy policy: https://nestdaddy.com/privacy

## Credentials

Your NestDaddy API key is stored by Dify's credential storage. The plugin uses it only in the `X-API-Key` header of requests to `https://nestdaddy.com`. It is never logged, included in error messages, or sent anywhere else.

## Third parties

The plugin talks only to NestDaddy. No other third-party service receives data from it.
