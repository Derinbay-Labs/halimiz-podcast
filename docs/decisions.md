# Standing product decisions

CEO decisions made in the claude.ai Desktop project "Bültenler" (Nov 2026). They were moved here
when management moved to Claude Code on 2026-11-21. Treat them as settled; a change needs a CEO
decision issue.

## Product

- Name "HAL'imiz Ne Olacak?". The publisher field is plain "Derinbay Labs". Site:
  https://halimiz.derinbay.com.
- Source: the daily "AI & Teknoloji Bülteni" (Claude Docs, one doc per month, e.g.
  "AI & Teknoloji Bülteni - 2026.11"). It becomes a NotebookLM audio overview.
- One episode a day, published at 07:00 Istanbul. Past bulletins are not back-filled as episodes
  (a missed day of the running show is caught up).
- AI disclosure wording: "yapay zekâ yardımı ile hazırlanır/hazırlanmıştır". Never use
  "yapay zekâ ile üretilir".
- Fully autonomous: no human review before publishing, and social posts go out without CEO
  approval. Never add an approval gate.

## Hosting and measurement

- Free and self-hosted: audio on GitHub Releases, the RSS feed and site on GitHub Pages
  (`tools/publish.py`, `.github/workflows/publish.yml`). No paid podcast host. DNS for
  derinbay.com is on Cloudflare.
- Downloads go through the OP3 prefix (podcast guid `ed974b2e-9ded-53a9-b6ef-8a43cbb481e2`).
  The site uses Cloudflare Web Analytics.
- The metrics panel is https://panel.derinbay.com, a Cloudflare Worker (`halimiz-panel`). Its data
  comes from `panel/data/metrics.json`, written by the metrics routine.
- Search: the site is in Google Search Console and Bing Webmaster Tools, with the sitemap
  submitted to both.
- Directories: Podcast Index feed 8098838. Spotify and Apple Podcasts are listed.
- YouTube: @halimizpodcast has imported the RSS feed since 11 Nov, starting with 8 Nov. Episodes
  3–7 Nov were uploaded by hand as plain videos. The YouTube check routine publishes any episode
  the import misses.

## Channels and distribution

- Use only podcast-only channels: handle `halimizpodcast`, address podcast@derinbay.com, and
  linkedin.com/company/halimizpodcast. Never use the CEO's personal accounts. The CEO opens new
  accounts; agents fill in the profiles.
- Instagram: Meta permanently closed @halimizpodcast on 2026-11-20, most likely for browser
  automation posting Reels from a brand-new account. The CEO decided on 2026-11-21 to open the
  business account @halimiz.podcast and keep posting through Chrome, paced: no Reels for the
  first three days, at most one a day until 2026-12-04, random start delay and waits between
  actions. Posts end in "profildeki link".
- Browser: the metrics and noon distribution routines use the dedicated kobe Chrome profile
  `HALimiz`, which holds only the podcast accounts. The YouTube subscriber count comes from the
  YouTube Data API (GCP project `halimiz-podcast-derinbay`, secret `YOUTUBE_API_KEY`).
- Link order in posts:
  - LinkedIn: the episode link first, so it becomes the preview card, then "Spotify'da takip et".
  - X: the episode link last, after Spotify.
  - Shorts: both links.
- Email newsletter: Buttondown, list `halimiz`. The publish workflow sends each episode. The repo
  secret is `BUTTONDOWN_API_KEY`.
- Postiz was rejected because its stack is heavy and it needs a Meta review; the agents post
  through Chrome.
- Site content: a glossary under `/sozluk/`, weekly and monthly archive pages, and per-topic
  "Son durum" paragraphs, refreshed weekly by `agents/haftalik-icerik.md`.

## Marketing

- Budget: 10,000 TL. Agents run the ads autonomously and the panel tracks them. The plan is the
  Claude Docs doc "HAL'imiz Ne Olacak? — Pazarlama ve Reklam Planı".
- 90-day target: 500 regular listeners and 300 downloads per day.
- Language: Turkish only for now.
  - Proposed, not decided: a one-week English pilot in early December on a separate feed
    (`/en/feed.xml`), without ads.
  - Proposed, not decided: targeting Turkish speakers in DE, NL and AT with ads.
