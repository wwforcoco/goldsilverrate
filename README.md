# GoldSilverRate.pk

Daily gold and silver Sarafa market benchmark rates for Pakistan.
Pure HTML/CSS/vanilla JS static site for Cloudflare Pages – no build step needed.

## Daily rate update (1 minute)

1. Open `data/rates.json`
2. Change the numbers and the `last_updated` line
3. Commit and push – every page, table, schema and the calculator update automatically

## Deploy on Cloudflare Pages

1. Workers & Pages → Create → Pages → Connect to Git → select this repo
2. Build command: (leave empty)
3. Build output directory: `/`
4. Deploy, then bind the custom domain `goldsilverrate.pk` in the Pages project settings

## Structure

- `data/rates.json` – the single source of truth for all rates
- `js/app.js` – rate engine, hydration, calculator (tola/masha/ratti/gram), kaat estimator
- `css/style.css` – dark bullion theme
- 15 SEO pages + about/contact/privacy/disclaimer + 404

## Notes

- WhatsApp CTA: paste your number into `whatsapp_number` in `data/rates.json` to activate
  the green WhatsApp buttons on bar pages. Empty = buttons stay hidden.
- Contact page email: replace `your-email@gmail.com` with your real address before AdSense review.
