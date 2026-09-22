import { Link, useNavigate } from "@tanstack/react-router";
import { FormEvent, useEffect, useMemo, useState, type ReactNode } from "react";
import { Heart, MapPin, Search, ShoppingCart } from "lucide-react";
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
  const firstName = user?.displayName?.split(" ")[0];

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

  function toTop() {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return (
    <div className="min-h-screen bg-bg text-fg" dir={lang === "ar" ? "rtl" : "ltr"} lang={lang}>
      {live ? (
        <Link
          to="/shop"
          search={{ flash: true }}
          className="block bg-gold py-1.5 text-center text-xs font-semibold tracking-wide text-wine"
        >
          {t.live} · {flash.title} — {flash.discount}% {lang === "ar" ? "خصم" : "off"}
        </Link>
      ) : null}

      <header className="sticky top-0 z-40 bg-wine text-cream">
        <div className="store-wrap flex items-center gap-3 py-2">
          <Logo compact invert className="shrink-0 px-1" />

          <label className="hidden min-w-24 shrink-0 cursor-pointer rounded-sm px-2 py-1 hover:outline hover:outline-1 hover:outline-gold sm:block">
            <span className="flex items-center gap-1 text-xs text-gold">
              <MapPin className="size-3.5" />
              {t.deliverTo}
            </span>
            <select
              value={area}
              onChange={(e) => setArea(e.target.value)}
              className="w-full bg-transparent text-sm font-bold text-cream outline-none"
            >
              {QATAR_AREAS.map((a) => (
                <option key={a} className="text-ink">
                  {a}
                </option>
              ))}
            </select>
          </label>

          <form onSubmit={onSearch} className="relative hidden min-w-0 flex-1 md:block">
            <div className="search-combo">
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
                autoComplete="off"
              />
              <button type="submit" aria-label={t.go}>
                <Search className="size-5" />
              </button>
            </div>
            {open && suggestions.length > 0 ? (
              <ul className="absolute inset-x-0 top-12 z-50 overflow-hidden rounded-md bg-card text-fg shadow-pop">
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
          </form>

          <div className="ms-auto flex items-center gap-1 text-sm">
            <div className="hidden h-11 items-center px-2 text-xs font-bold hover:outline hover:outline-1 hover:outline-gold sm:flex" role="group" aria-label="Language">
              <button type="button" onClick={() => setLang("en")} className={lang === "en" ? "text-gold" : "text-cream/70"}>
                EN
              </button>
              <span className="mx-1 text-cream/40">|</span>
              <button type="button" onClick={() => setLang("ar")} className={lang === "ar" ? "text-gold" : "text-cream/70"}>
                AR
              </button>
            </div>

            <Link
              to={user ? "/account" : "/login"}
              className="hidden min-w-24 flex-col justify-center rounded-sm px-2 py-1 leading-tight hover:outline hover:outline-1 hover:outline-gold md:flex"
            >
              <span className="text-xs text-cream/80">
                {user ? `${t.hello}, ${firstName ?? t.account}` : t.helloSignIn}
              </span>
              <span className="text-sm font-bold">{t.lists}</span>
            </Link>

            <Link
              to={user ? "/account" : "/login"}
              className="hidden flex-col justify-center rounded-sm px-2 py-1 leading-tight hover:outline hover:outline-1 hover:outline-gold lg:flex"
            >
              <span className="text-xs text-cream/80">{t.returns}</span>
              <span className="text-sm font-bold">{t.orders}</span>
            </Link>

            {isPending ? null : user && isAdminEmail(user.primaryEmail) ? (
              <Link
                to="/admin"
                className="hidden rounded-sm px-2 py-2 text-xs font-bold text-gold hover:outline hover:outline-1 hover:outline-gold lg:inline"
              >
                {t.admin}
              </Link>
            ) : null}

            <Link to="/wishlist" className="relative grid size-11 place-items-center rounded-sm hover:outline hover:outline-1 hover:outline-gold" aria-label={t.wishlist}>
              <Heart className="size-5" />
              {wishCount > 0 ? <Badge n={wishCount} /> : null}
            </Link>

            <Link to="/cart" className="relative flex h-11 items-end gap-1 rounded-sm px-2 pb-1 hover:outline hover:outline-1 hover:outline-gold" aria-label={t.cart}>
              <span className="relative">
                <ShoppingCart className="size-7" />
                <span className="absolute -top-1 inset-x-0 text-center text-sm font-bold text-gold">
                  {count}
                </span>
              </span>
              <span className="hidden pb-0.5 text-sm font-bold sm:inline">{t.cart}</span>
            </Link>
          </div>
        </div>

        <form onSubmit={onSearch} className="px-4 pb-2 md:hidden">
          <div className="search-combo">
            <input name="q" value={q} onChange={(e) => setQ(e.target.value)} placeholder={t.search} />
            <button type="submit" aria-label={t.go}>
              <Search className="size-5" />
            </button>
          </div>
        </form>

        <nav className="bg-ink">
          <div className="store-wrap flex gap-1 overflow-x-auto py-1.5 text-sm">
            <Link to="/shop" className="whitespace-nowrap rounded-sm px-2 py-1.5 font-semibold hover:outline hover:outline-1 hover:outline-gold">
              {t.all}
            </Link>
            {live ? (
              <Link
                to="/shop"
                search={{ flash: true }}
                className="whitespace-nowrap rounded-sm px-2 py-1.5 font-semibold text-gold hover:outline hover:outline-1 hover:outline-gold"
              >
                {t.flash}
              </Link>
            ) : null}
            {CATEGORIES.map((c) => (
              <Link
                key={c.id}
                to="/shop"
                search={{ category: c.id }}
                className="whitespace-nowrap rounded-sm px-2 py-1.5 hover:outline hover:outline-1 hover:outline-gold"
              >
                {lang === "ar" ? c.nameAr : c.name}
              </Link>
            ))}
            <Link to="/faq" className="ms-auto hidden whitespace-nowrap rounded-sm px-2 py-1.5 text-gold lg:inline">
              {t.service}
            </Link>
          </div>
        </nav>
      </header>

      <main>{children}</main>

      <button
        type="button"
        onClick={toTop}
        className="mt-10 block w-full bg-wine py-3 text-center text-sm font-semibold text-cream hover:bg-ink"
      >
        {t.backToTop}
      </button>
      <footer className="bg-ink text-cream">
        <div className="store-wrap grid gap-8 py-12 sm:grid-cols-2 lg:grid-cols-4">
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
            <Link to="/account">{t.orders}</Link>
          </FooterCol>
          <FooterCol title={t.categories}>
            {CATEGORIES.map((c) => (
              <Link key={c.id} to="/shop" search={{ category: c.id }}>
                {lang === "ar" ? c.nameAr : c.name}
              </Link>
            ))}
          </FooterCol>
        </div>
        <div className="border-t border-cream/10">
          <div className="store-wrap flex flex-wrap items-center justify-between gap-3 py-4 text-sm text-gold/80">
            <span>© {new Date().getFullYear()} 11-11 · <Link to="/privacy">{t.privacy}</Link> · <Link to="/terms">{t.terms}</Link></span>
            <span>QAR · COD · SkipCash</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

function Badge({ n }: { n: number }) {
  return (
    <span className="absolute end-1 top-1 grid min-w-4 place-items-center rounded-full bg-gold px-1 text-xs font-bold text-wine">
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
