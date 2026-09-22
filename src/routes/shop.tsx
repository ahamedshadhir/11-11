import { createFileRoute, Link } from "@tanstack/react-router";
import { Shell } from "@/components/layout";
import { ProductCard } from "@/components/product-card";
import { CATEGORIES, byCategory, searchProducts } from "@/lib/catalog";
import { COPY } from "@/lib/i18n";
import { flashLive, useStore } from "@/lib/store";
import { useMemo, useState } from "react";

export type ShopSearch = { q?: string; category?: string; flash?: boolean };

export const Route = createFileRoute("/shop")({
  validateSearch: (s: Record<string, unknown>): ShopSearch => ({
    q: typeof s.q === "string" && s.q.length ? s.q : undefined,
    category: typeof s.category === "string" && s.category.length ? s.category : undefined,
    flash: s.flash === true || s.flash === "true" ? true : undefined,
  }),
  component: Shop,
});

function Shop() {
  const { q, category, flash: flashOnly } = Route.useSearch();
  const lang = useStore((s) => s.lang);
  const flash = useStore((s) => s.flash);
  const t = COPY[lang];
  const [sort, setSort] = useState<"featured" | "low" | "high">("featured");
  const live = flashLive(flash);

  const items = useMemo(() => {
    let list = q ? searchProducts(q) : byCategory(category);
    if (flashOnly && live) list = list.filter((p) => flash.productIds.includes(p.id));
    if (sort === "low") list = [...list].sort((a, b) => a.price - b.price);
    if (sort === "high") list = [...list].sort((a, b) => b.price - a.price);
    return list;
  }, [q, category, flashOnly, live, flash.productIds, sort]);

  const heading =
    flashOnly && live
      ? flash.title
      : q
        ? q
        : category
          ? (lang === "ar"
              ? CATEGORIES.find((c) => c.id === category)?.nameAr
              : CATEGORIES.find((c) => c.id === category)?.name) ?? t.shop
          : t.shop;

  return (
    <Shell>
      <div className="store-wrap grid gap-8 py-6 lg:grid-cols-[220px_1fr]">
        <aside className="lg:border-e lg:border-line lg:pe-6">
          <h4 className="text-sm font-bold">{t.categories}</h4>
          <ul className="mt-3 space-y-1 text-sm">
            {live ? (
              <li>
                <Link
                  to="/shop"
                  search={{ flash: true }}
                  className={flashOnly ? "font-semibold text-gold" : "hover:text-gold"}
                >
                  {t.flash}
                </Link>
              </li>
            ) : null}
            <li>
              <Link to="/shop" className={!category && !flashOnly && !q ? "font-semibold text-wine" : "hover:text-gold"}>
                {t.all}
              </Link>
            </li>
            {CATEGORIES.map((c) => (
              <li key={c.id}>
                <Link
                  to="/shop"
                  search={{ category: c.id }}
                  className={category === c.id ? "font-semibold text-wine" : "hover:text-gold"}
                >
                  {lang === "ar" ? c.nameAr : c.name}
                </Link>
              </li>
            ))}
          </ul>
        </aside>
        <div>
          <div className="flex flex-wrap items-end justify-between gap-3 border-b border-line pb-3">
            <div>
              <h1 className="text-xl font-bold text-ink">{heading}</h1>
              <p className="mt-1 text-sm text-muted">
                {items.length} {t.results}
              </p>
            </div>
            <label className="text-sm text-muted">
              {t.sort}
              <select
                value={sort}
                onChange={(e) => setSort(e.target.value as typeof sort)}
                className="ms-2 h-11 rounded-md border border-line bg-card px-2 text-fg"
              >
                <option value="featured">{t.featured}</option>
                <option value="low">{t.low}</option>
                <option value="high">{t.high}</option>
              </select>
            </label>
          </div>
          <div className="mt-4 grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-4">
            {items.map((p) => (
              <ProductCard key={p.id} p={p} />
            ))}
          </div>
          {items.length === 0 ? <p className="mt-8 text-muted">{t.noItems}</p> : null}
        </div>
      </div>
    </Shell>
  );
}
