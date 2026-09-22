import { createFileRoute, Link } from "@tanstack/react-router";
import { Countdown } from "@/components/countdown";
import { Shell } from "@/components/layout";
import { ProductCard } from "@/components/product-card";
import { Button } from "@/components/ui/button";
import { CATEGORIES, HERO_IMAGE, PRODUCTS, byCategory } from "@/lib/catalog";
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
  const fashion = byCategory("fashion").slice(0, 8);
  const home = byCategory("home").slice(0, 8);

  return (
    <Shell>
      <section className="bg-wine text-cream">
        <div className="store-wrap grid items-center gap-6 py-5 lg:grid-cols-[1.1fr_0.9fr] lg:py-6">
          <div>
            <p className="text-xs font-semibold uppercase tracking-widest text-gold">11-11 Qatar</p>
            {live ? (
              <>
                <h1 className="mt-2 font-display text-4xl font-semibold leading-tight tracking-tight lg:text-5xl">
                  {flash.title} — {flash.discount}% off
                </h1>
                <p className="mt-4 max-w-md text-cream/80">{t.heroText}</p>
                <div className="mt-6">
                  <Countdown endsAt={flash.endsAt} />
                </div>
                <Button asChild variant="gold" className="mt-6">
                  <Link to="/shop" search={{ flash: true }}>
                    {t.shopNow}
                  </Link>
                </Button>
              </>
            ) : (
              <>
                <h1 className="mt-2 font-display text-4xl font-semibold leading-tight tracking-tight lg:text-5xl">
                  {t.heroTitle}
                </h1>
                <p className="mt-4 max-w-md text-cream/80">{t.heroText}</p>
                <Button asChild variant="gold" className="mt-6">
                  <Link to="/shop">{t.shopNow}</Link>
                </Button>
              </>
            )}
          </div>
          <div className="rounded-md bg-card p-6">
            <div className="packshot mx-auto h-48 lg:h-56">
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

      <section className="store-wrap -mt-8 pb-4">
        <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
          {CATEGORIES.map((c) => (
            <Link
              key={c.id}
              to="/shop"
              search={{ category: c.id }}
              className="bg-card p-4 shadow-card transition-[box-shadow] duration-150 hover:shadow-card-hover"
            >
              <h2 className="text-sm font-bold text-ink">{lang === "ar" ? c.nameAr : c.name}</h2>
              <span className="packshot mt-3 h-28">
                <img src={c.image} alt="" loading="lazy" />
              </span>
              <span className="mt-3 block text-xs font-semibold text-wine">{t.seeMore}</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="store-wrap py-8">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <h2 className="text-xl font-bold text-ink">{live ? t.deals : t.shop}</h2>
          {live ? <Countdown endsAt={flash.endsAt} /> : null}
        </div>
        <div className="mt-4 grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-4">
          {deals.map((p) => (
            <ProductCard key={p.id} p={p} />
          ))}
        </div>
      </section>

      <DepartmentRow title={lang === "ar" ? "أزياء" : "Fashion"} category="fashion" items={fashion} more={t.seeMore} />
      <DepartmentRow title={lang === "ar" ? "المنزل والمطبخ" : "Home & Kitchen"} category="home" items={home} more={t.seeMore} />
    </Shell>
  );
}

function DepartmentRow({
  title,
  category,
  items,
  more,
}: {
  title: string;
  category: string;
  items: typeof PRODUCTS;
  more: string;
}) {
  if (!items.length) return null;
  return (
    <section className="store-wrap pb-10">
      <div className="flex items-end justify-between gap-4">
        <h2 className="text-xl font-bold text-ink">{title}</h2>
        <Link to="/shop" search={{ category }} className="text-sm font-semibold text-wine hover:underline">
          {more}
        </Link>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-4">
        {items.map((p) => (
          <ProductCard key={p.id} p={p} />
        ))}
      </div>
    </section>
  );
}
