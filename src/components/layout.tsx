import { Link, useNavigate } from "@tanstack/react-router";
import { FormEvent, useEffect, useMemo, useState, type ReactNode } from "react";
import { Heart, Search, ShoppingBag, UserRound } from "lucide-react";
import { UserButton } from "@/lib/auth/gates";
import { useCurrentUserState } from "@/lib/auth/use-current-user";
import { isAdminEmail } from "@/lib/admin";
import { CATEGORIES, QATAR_AREAS, searchProducts } from "@/lib/catalog";
import { COPY } from "@/lib/i18n";
import { cartCount, flashLive, useStore } from "@/lib/store";
import { Logo } from "./logo";

export function Shell({ children }: { children: ReactNode }) {
  const lang = useStore((s) => s.lang);
  const setLang = useStore((s) => s.setLang);
  const area = useStore((s) => s.area);
  const setArea = useStore((s) => s.setArea);
  const cart = useStore((s) => s.cart);
  const flash = useStore((s) => s.flash);
  const wish = useStore((s) => s.wish);
  const t = COPY[lang];
  const nav = useNavigate();
  const { user, isPending } = useCurrentUserState();
  const [ready, setReady] = useState(false);
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(false);
  const live = flashLive(flash);
  const count = ready ? cartCount(cart) : 0;
  const wishCount = ready ? wish.length : 0;

  useEffect(() => {
    const unsub = useStore.persist.onFinishHydration(() => setReady(true));
    if (useStore.persist.hasHydrated()) setReady(true);
    return unsub;
  }, []);

  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
  }, [lang]);

  const suggestions = useMemo(() => (q.trim().length > 1 ? searchProducts(q).slice(0, 6) : []), [q]);

  function onSearch(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setOpen(false);
    void nav({ to: "/shop", search: { q: q.trim() || undefined } });
  }

  return (
    <div className="min-h-screen bg-bg text-fg" dir={lang === "ar" ? "rtl" : "ltr"} lang={lang}>
      {live ? (
        <Link
          to="/shop"
          search={{ flash: true }}
          className="block bg-wine py-2 text-center text-xs font-semibold tracking-wide text-gold"
        >
          {t.live} · {flash.title} — {flash.discount}% {lang === "ar" ? "خصم" : "off"}
        </Link>
      ) : null}
      <header className="sticky top-0 z-40 border-b border-line bg-card/95 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center gap-3 px-4 py-3">
          <Logo className="shrink-0" />
          <form onSubmit={onSearch} className="relative hidden min-w-0 flex-1 items-center gap-3 md:flex">
            <label className="hidden shrink-0 text-xs text-muted lg:block">
              {t.deliverTo}
              <select
                value={area}
                onChange={(e) => setArea(e.target.value)}
                className="ms-1 bg-transparent font-semibold text-wine outline-none"
              >
                {QATAR_AREAS.map((a) => (
                  <option key={a}>{a}</option>
                ))}
              </select>
            </label>
            <div className="relative min-w-0 flex-1">
              <input
                name="q"
                value={q}
                onChange={(e) => {
                  setQ(e.target.value);
                  setOpen(true);
                }}
                onFocus={() => setOpen(true)}
                onBlur={() => setTimeout(() => setOpen(false), 180)}
                placeholder={t.search}
                className="field rounded-full bg-cream pe-12"
                autoComplete="off"
              />
              <button
                type="submit"
                className="absolute end-1 top-1 grid size-9 place-items-center rounded-full bg-wine text-cream"
                aria-label={t.go}
              >
                <Search className="size-4" />
              </button>
              {open && suggestions.length > 0 ? (
                <ul className="absolute inset-x-0 top-12 z-50 overflow-hidden rounded-xl bg-card shadow-pop">
                  {suggestions.map((p) => (
                    <li key={p.id}>
                      <Link
                        to="/product/$slug"
                        params={{ slug: p.slug }}
                        className="flex items-center gap-3 px-3 py-2 hover:bg-cream"
                        onMouseDown={(e) => e.preventDefault()}
                      >
                        <img src={p.image} alt="" className="size-10 object-contain" />
                        <span className="text-sm">{p.name}</span>
                      </Link>
                    </li>
                  ))}
                </ul>
              ) : null}
            </div>
          </form>
          <div className="ms-auto flex items-center gap-1 text-sm">
            <div className="flex h-11 items-center gap-1 px-1 text-xs font-semibold" role="group" aria-label="Language">
              <button
                type="button"
                onClick={() => setLang("en")}
                className={lang === "en" ? "text-wine" : "text-muted"}
              >
                EN
              </button>
              <span className="text-line">/</span>
              <button
                type="button"
                onClick={() => setLang("ar")}
                className={lang === "ar" ? "text-wine" : "text-muted"}
              >
                AR
              </button>
            </div>
            <Link to="/wishlist" className="relative grid size-11 place-items-center" aria-label={t.wishlist}>
              <Heart className="size-5" />
              {wishCount > 0 ? <Badge n={wishCount} /> : null}
            </Link>
            <Link to="/cart" className="relative grid size-11 place-items-center" aria-label={t.cart}>
              <ShoppingBag className="size-5" />
              {count > 0 ? <Badge n={count} /> : null}
            </Link>
            {isPending ? (
              <div className="h-8 w-16 animate-pulse rounded-md bg-line" />
            ) : user ? (
              <div className="flex items-center gap-1">
                {isAdminEmail(user.primaryEmail) ? (
                  <Link to="/admin" className="hidden rounded-md px-2 text-xs font-semibold text-gold sm:inline">
                    {t.admin}
                  </Link>
                ) : null}
                <Link to="/account" className="grid size-11 place-items-center sm:hidden" aria-label={t.account}>
                  <UserRound className="size-5" />
                </Link>
                <div className="hidden sm:block">
                  <UserButton />
                </div>
              </div>
            ) : (
              <Link
                to="/login"
                className="rounded-md bg-wine px-3 py-2 font-semibold text-cream"
              >
                {t.login}
              </Link>
            )}
          </div>
        </div>
        <form onSubmit={onSearch} className="px-4 pb-3 md:hidden">
          <div className="relative">
            <input
              name="q"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder={t.search}
              className="field rounded-full bg-cream pe-12"
            />
            <button
              type="submit"
              className="absolute end-1 top-1 grid size-9 place-items-center rounded-full bg-wine text-cream"
              aria-label={t.go}
            >
              <Search className="size-4" />
            </button>
          </div>
        </form>
        <nav className="mx-auto flex max-w-6xl gap-1 overflow-x-auto px-4 pb-3 text-sm">
          <Link
            to="/shop"
            className="whitespace-nowrap rounded-full px-3 py-2 hover:bg-cream"
          >
            {t.all}
          </Link>
          {live ? (
            <Link
              to="/shop"
              search={{ flash: true }}
              className="whitespace-nowrap rounded-full px-3 py-2 font-semibold text-gold hover:bg-cream"
            >
              {t.flash}
            </Link>
          ) : null}
          {CATEGORIES.map((c) => (
            <Link
              key={c.id}
              to="/shop"
              search={{ category: c.id }}
              className="whitespace-nowrap rounded-full px-3 py-2 hover:bg-cream"
            >
              {lang === "ar" ? c.nameAr : c.name}
            </Link>
          ))}
        </nav>
      </header>
      <main>{children}</main>
      <footer className="mt-16 bg-ink text-cream">
        <div className="mx-auto grid max-w-6xl gap-8 px-4 py-12 sm:grid-cols-2 lg:grid-cols-5">
          <div>
            <Logo invert />
            <p className="mt-4 max-w-[28ch] text-sm text-gold/80">{t.tagline}</p>
          </div>
          <FooterCol title={t.about}>
            <Link to="/about">{t.about}</Link>
            <Link to="/shop">{t.viewAll}</Link>
          </FooterCol>
          <FooterCol title={t.service}>
            <Link to="/contact">{t.contact}</Link>
            <Link to="/faq">{t.faq}</Link>
          </FooterCol>
          <FooterCol title={t.categories}>
            {CATEGORIES.slice(0, 5).map((c) => (
              <Link key={c.id} to="/shop" search={{ category: c.id }}>
                {lang === "ar" ? c.nameAr : c.name}
              </Link>
            ))}
          </FooterCol>
          <FooterCol title={t.legal}>
            <Link to="/privacy">{t.privacy}</Link>
            <Link to="/terms">{t.terms}</Link>
            {user ? <Link to="/admin">{t.admin}</Link> : null}
          </FooterCol>
        </div>
        <div className="mx-auto flex max-w-6xl justify-between border-t border-cream/10 px-4 py-4 text-sm text-gold/80">
          <span>© {new Date().getFullYear()} 11-11</span>
          <span>QAR · COD · SkipCash</span>
        </div>
      </footer>
    </div>
  );
}

function Badge({ n }: { n: number }) {
  return (
    <span className="absolute end-1 top-1 grid min-w-4 place-items-center rounded-full bg-wine px-1 text-[0.6rem] font-bold text-cream">
      {n}
    </span>
  );
}

function FooterCol({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="flex flex-col gap-2 text-sm">
      <p className="text-xs font-semibold uppercase tracking-widest text-gold">{title}</p>
      {children}
    </div>
  );
}
