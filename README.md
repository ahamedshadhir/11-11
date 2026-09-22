# 11-11

Qatar store for electronics, fashion and home. Wine `#420e15`, gold `#be923b`, cream `#f6f3ee`. Logo is **11:11** over **eleven-eleven**.

## Stack

TanStack Start · React 19 · Tailwind v4 · Better Auth · Postgres (Neon in production, PGLite locally)

## Features

- 87 matching studio product photos across 8 departments (4 phones)
- Amazon-style store chrome (wine header, gold search, department tiles)
- Flash sale with countdown
- Cart, wishlist, COD + SkipCash checkout
- English / العربية
- Account + separate `/admin` console (no store header)
- Sign in with Google, X, or email

## Local

```bash
npm install
npm run dev
```

## Deploy

Vercel runs `npm run build` (Nitro `vercel` preset). Set `DATABASE_URL` (Neon) on the project. Auth uses the app’s Better Auth at `/api/auth/*`.
