# 11-11 store

Flask shop for Qatar (QAR). Live: https://elevenelven.vercel.app/

## Local

```powershell
python -m venv .venv
.\.​venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

Demo: `demo@1111.local` / `demo123`  
Admin: `admin@1111.local` / `admin123` → `/admin`  
Coupon: `FLASH10`

## Backend routes

- `GET /` homepage
- `GET /shop` catalog, `?q=` `?category=` `?brand=` `?sort=`
- `GET /product/<id>/<slug>`
- `GET|POST /login` `/register` `/logout`
- `GET /cart` `/wishlist` `/checkout`
- `GET /api/cart` `POST /api/cart/add|update|remove`
- `POST /api/wishlist/toggle` `GET /api/search` `POST /api/coupon`
- `GET|POST /track` `/account` `/account/orders` `/admin`

Vercel uses SQLite in `/tmp` (demo only). Orders and logins can reset on a cold start. Use Neon/Supabase for real persistence.
