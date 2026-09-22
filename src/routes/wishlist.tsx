import { createFileRoute, Link } from "@tanstack/react-router";
import { Heart } from "lucide-react";
import { Shell } from "@/components/layout";
import { ProductCard } from "@/components/product-card";
import { Button } from "@/components/ui/button";
import { PRODUCTS } from "@/lib/catalog";
import { COPY } from "@/lib/i18n";
import { useHydrated, useStore } from "@/lib/store";

export const Route = createFileRoute("/wishlist")({ component: Wishlist });

function Wishlist() {
  const lang = useStore((s) => s.lang);
  const wish = useStore((s) => s.wish);
  const t = COPY[lang];
  const ready = useHydrated();
  const items = PRODUCTS.filter((p) => wish.includes(p.id));

  return (
    <Shell>
      <div className="mx-auto max-w-6xl px-4 py-10">
        <h1 className="font-display text-3xl font-semibold text-wine">{t.wishlist}</h1>
        {!ready ? (
          <div className="mt-6 h-40 animate-pulse rounded-xl bg-line" />
        ) : items.length === 0 ? (
          <div className="mt-10 rounded-xl bg-card px-6 py-16 text-center shadow-card">
            <Heart className="mx-auto size-10 text-gold" />
            <p className="mt-4 text-muted">{t.emptyWish}</p>
            <Button asChild className="mt-6">
              <Link to="/shop">{t.shop}</Link>
            </Button>
          </div>
        ) : (
          <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
            {items.map((p) => (
              <ProductCard key={p.id} p={p} />
            ))}
          </div>
        )}
      </div>
    </Shell>
  );
}
