# 11-11

Qatar store for electronics, fashion and home. Wine `#420e15`, gold `#be923b`, cream `#f6f3ee`. Logo is **11:11** over **eleven-eleven**.

## Stack

TanStack Start · React 19 · Tailwind v4 · Better Auth · Postgres (Neon in production, PGLite locally)

## Features

- 87 matching studio product photos across 8 departments (4 phones)
- Amazon-style store chrome (wine header, gold search, department tiles)
- Flash sale with countdown
- Cart, wishlist, cash on delivery + SkipCash
- Printable purchase receipts
- English / العربية
- Account + separate `/admin` console (orders from the database)
- Sign in with Google, X, or email (`admin@1111.local` / `admin123` for the store console)

Checkout requires a signed-in account so every order is saved. SkipCash uses the live gateway when `SKIPCASH_KEY_ID` and `SKIPCASH_KEY_SECRET` are set on Vercel; otherwise a hosted card page completes payment without storing card numbers.

## Local

```bash
npm install
npm run dev
```

## Deploy

Vercel runs `npm run build` (Nitro `vercel` preset). Set `DATABASE_URL` (Neon) on the project. Auth uses the app’s Better Auth at `/api/auth/*`. Optional SkipCash: `SKIPCASH_KEY_ID`, `SKIPCASH_KEY_SECRET`, `SKIPCASH_CLIENT_ID`, `SKIPCASH_WEBHOOK_KEY`.
