import { createFileRoute, Link } from "@tanstack/react-router";
import { Countdown } from "@/components/countdown";
import { Shell } from "@/components/layout";
import { ProductCard } from "@/components/product-card";
import { Button } from "@/components/ui/button";
import { CATEGORIES, HERO_IMAGE, PRODUCTS } from "@/lib/catalog";
import { COPY } from "@/lib/i18n";
import { flashLive, useStore } from "@/lib/store";

export const Route = createFileRoute("/")({ component: Home });

function Home() {
  const lang = useStore((s) => s.lang);
  const flash = useStore((s) => s.flash);
  const t = COPY[lang];
  const live = flashLive(flash);
  const deals = live
    ? PRODUCTS.filter((p) => flash.productIds.includes(p.id)).slice(0, 8)
    : PRODUCTS.slice(0, 8);
  const fresh = PRODUCTS.filter((p) => !deals.some((d) => d.id === p.id)).slice(0, 8);

  return (
    <Shell>
      <section className="bg-cream">
        <div className="mx-auto grid max-w-6xl items-center gap-8 px-4 py-10 lg:grid-cols-2 lg:py-16">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">11-11 Qatar</p>
            {live ? (
              <>
                <p className="mt-3 text-xs font-bold tracking-widest text-wine">{t.live}</p>
                <h1 className="mt-1 font-display text-4xl font-semibold leading-tight tracking-tight text-ink lg:text-5xl">
                  {flash.title} — {flash.discount}% off
                </h1>
                <p className="mt-4 max-w-md text-muted">{t.heroText}</p>
                <div className="mt-6">
                  <Countdown endsAt={flash.endsAt} />
                </div>
                <Button asChild className="mt-6">
                  <Link to="/shop" search={{ flash: true }}>
                    {t.shopNow}
                  </Link>
                </Button>
              </>
            ) : (
              <>
                <h1 className="mt-3 font-display text-4xl font-semibold leading-tight tracking-tight text-ink lg:text-5xl">
                  {t.heroTitle}
                </h1>
                <p className="mt-4 max-w-md text-muted">{t.heroText}</p>
                <Button asChild className="mt-6">
                  <Link to="/shop">{t.shopNow}</Link>
                </Button>
              </>
            )}
          </div>
          <div className="rounded-xl bg-card p-6 shadow-card">
            <div className="packshot mx-auto h-72 lg:h-80">
              <img
                src={HERO_IMAGE}
                alt="AirPods Max Silver"
                width={720}
                height={720}
                decoding="async"
              />
            </div>
          </div>
        </div>
      </section>
      <section className="mx-auto max-w-6xl px-4 py-12">
        <div className="flex items-end justify-between gap-4">
          <h2 className="font-display text-2xl font-semibold text-wine">{t.shopByCategory}</h2>
          <Link to="/shop" className="text-sm text-gold">
            {t.viewAll}
          </Link>
        </div>
        <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-7">
          {CATEGORIES.map((c) => (
            <Link
              key={c.id}
              to="/shop"
              search={{ category: c.id }}
              className="rounded-lg bg-card p-3 text-center shadow-card transition-[box-shadow] duration-150 hover:shadow-card-hover"
            >
              <span className="packshot h-28">
                <img src={c.image} alt="" loading="lazy" />
              </span>
              <span className="mt-2 block text-xs font-medium">
                {lang === "ar" ? c.nameAr : c.name}
              </span>
            </Link>
          ))}
        </div>
      </section>
      <section className="bg-card/60 py-12">
        <div className="mx-auto max-w-6xl px-4">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <h2 className="font-display text-2xl font-semibold text-wine">
              {live ? t.deals : t.viewAll}
            </h2>
            {live ? <Countdown endsAt={flash.endsAt} /> : null}
          </div>
          <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
            {deals.map((p) => (
              <ProductCard key={p.id} p={p} />
            ))}
          </div>
        </div>
      </section>
      {fresh.length ? (
        <section className="mx-auto max-w-6xl px-4 py-12">
          <h2 className="font-display text-2xl font-semibold text-wine">{t.newIn}</h2>
          <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
            {fresh.map((p) => (
              <ProductCard key={p.id} p={p} />
            ))}
          </div>
        </section>
      ) : null}
    </Shell>
  );
}
