# Vehicle Import Platform — outreach demo

A one-page product walkthrough for vehicle importers and dealers, with a live booking
calendar that creates a Google Meet, emails both sides and logs the lead.

```
index.html              the page (hosted version)
assets/                 screenshots (WebP), 13-second clip (WebM + MP4), poster, Open Graph image
dist/…Demo.html         self-contained single file for email attachments / offline
tools/build_single_file.py   rebuilds dist/ from index.html + assets/
```

## Personalise a link per prospect

Every setting has a neutral default, so the bare link works for anyone. Add URL
parameters to tailor it:

| Parameter  | Default               | Changes                                                        |
|------------|-----------------------|----------------------------------------------------------------|
| `company`  | —                     | "Prepared for …" badge, page title, pre-filled Company field   |
| `currency` | your local currency   | Copy about revenue/costs and the currency stat (`EUR + USD`)   |
| `origin`   | China                 | Where vehicles are sourced ("from sourcing in Japan …")        |
| `market`   | —                     | Where they are sold ("customs clearance in Germany", route)    |
| `ref`      | —                     | Campaign tag stored with the booking (`source` column)         |

Example: `index.html?company=Acme%20Motors&currency=EUR&origin=Japan&market=Germany&ref=li-wave1`

Defaults live in the `CONFIG` block at the top of the script in `index.html`.

## Booking flow (n8n)

Workflow **Vehicle Import Platform - Booking API** (`qR6L75qHiUnsP0d2`, project *Futuristic Life*)
on `https://oussama19.app.n8n.cloud`.

| Endpoint | What it does |
|---|---|
| `GET  /webhook/vehicle-import/slots` | Reads free/busy from Google Calendar and returns open slots as UTC ISO strings. The page groups and labels them in the visitor's own time zone. |
| `POST /webhook/vehicle-import/book`  | Body `{name, email, company?, phone?, message?, start (ISO), tz, source?, website (honeypot)}`. Validates, re-checks the slot, creates a 20-min Google Meet event with the prospect invited, responds to the page, then appends the lead to the *Vehicle Import Demo Leads* sheet and sends two emails: a notification to oussama.g@oussamalabs.com and a confirmation to the prospect (reply-to oussama.g@oussamalabs.com). |

Responses: `200 {ok:true, when, meetLink}` · `400 invalid` · `409 slot taken` · `503 calendar unavailable`.
If slots can't be loaded, the page falls back to an email button.

Booking rules (edit at the top of the **Build Open Slots** and **Validate Booking** Code
nodes — keep both in sync): Sun–Thu, 09:00–17:00 Africa/Algiers, 30-min grid, 20-min calls,
14 days ahead, 12 h minimum notice.

## Rebuild the single-file version

```bash
python tools/build_single_file.py
```

## Deploy

Live on GitHub Pages: **https://oussamarevolotionary.github.io/vehicle-import-demo/**
(published from `main`, root folder). If the page moves to another host, update the
absolute `og:url` / `og:image` meta tags so link previews keep working in WhatsApp,
LinkedIn and email clients.
