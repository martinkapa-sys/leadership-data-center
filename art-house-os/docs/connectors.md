# Connectors

Start with **shop + image generation**; add the rest stage by stage. Keys go in environment secrets (see `.env.example`).

## Already in `.mcp.json` (official remote/hosted MCP servers)
| Server | Used by | Purpose |
|---|---|---|
| `replicate` | designer | FLUX / Ideogram / Recraft generation, Real-ESRGAN upscaling |
| `apify` | trend-scout | Etsy, Pinterest, Instagram, TikTok scrapers for research |
| `canva` | designer, merchandiser, social-manager | mockups, social templates, size-guide graphics |
| `stripe` | growth-analyst | payments data if you sell off-marketplace |
| `notion` | ops-chief (optional) | board view of the catalog / approvals |

## Add as claude.ai connectors (Settings → Connectors) — they then work in Claude Code too
Gmail (customer-care), Google Drive (asset storage), Slack (approval digest), Google Calendar (launch calendar).
Check the connector directory for Shopify, Klaviyo, Figma and Canva — use the official listing where one exists.

## Need an MCP server you add yourself (verify the current official option before installing)
| Service | Server name expected by agents/settings | Notes |
|---|---|---|
| Shopify Admin | `shopify` | products, drafts, orders, analytics. Shopify publishes official MCP servers; otherwise wrap the Admin GraphQL API. |
| Etsy | `etsy` | Open API v3 (OAuth, app approval required). No official MCP known — small custom server (listings, inventory, stats, receipts). |
| Printful / Gelato / Printify | `printful` | only if you sell physical prints. |
| Pinterest | `pinterest` | Pinterest API v5: boards, pins, analytics, ads. |
| Meta (Instagram/Facebook) | `meta` | Graph API: publish media, insights, comments; Marketing API for ads. |
| Buffer / Later | `buffer` | simpler alternative to the two above for scheduling. |
| Klaviyo | `klaviyo` | Klaviyo offers an official MCP server. |
| Google Analytics 4 | `ga4` | Google's analytics MCP server or the Data API. |

Keep the server names above so `.claude/settings.json` permissions and agent `tools:` lists match.
A custom MCP server is a ~200-line project — ask Claude: "build an Etsy MCP server with tools
list_listings, create_draft_listing, update_listing, get_stats, list_receipts".

## Safety
- Every server that can publish, send or spend is in the `ask` list in `.claude/settings.json`.
- `.claude/hooks/require_approval.py` blocks publishing tools unless the referenced SKU is `publish_approved`.
- `data/audit.log` records every MCP call.
