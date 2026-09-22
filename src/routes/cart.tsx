import { createFileRoute, Link } from "@tanstack/react-router";
import { ShoppingCart } from "lucide-react";
import { Shell } from "@/components/layout";
import { QtyStepper } from "@/components/qty-stepper";
import { Button } from "@/components/ui/button";
import { PRODUCTS } from "@/lib/catalog";
import { COPY } from "@/lib/i18n";
import { cartCount, cartTotal, salePrice, useHydrated, useStore } from "@/lib/store";
import { qar } from "@/lib/utils";

export const Route = createFileRoute("/cart")({ component: CartPage });

function CartPage() {
  const lang = useStore((s) => s.lang);
  const cart = useStore((s) => s.cart);
  const flash = useStore((s) => s.flash);
  const setQty = useStore((s) => s.setQty);
  const remove = useStore((s) => s.remove);
  const t = COPY[lang];
  const ready = useHydrated();
  const total = cartTotal(cart, flash);
  const count = cartCount(cart);

  return (
    <Shell>
      <div className="store-wrap py-8">
        <h1 className="text-2xl font-bold text-ink">{t.cart}</h1>
        {!ready ? (
          <div className="mt-6 h-40 animate-pulse rounded-md bg-line" />
        ) : cart.length === 0 ? (
          <div className="mt-8 bg-card px-6 py-16 text-center shadow-card">
            <ShoppingCart className="mx-auto size-10 text-gold" />
            <p className="mt-4 text-muted">{t.emptyCart}</p>
            <Button asChild className="mt-6">
              <Link to="/shop">{t.shop}</Link>
            </Button>
          </div>
        ) : (
          <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_280px]">
            <ul className="divide-y divide-line bg-card shadow-card">
              {cart.map((l) => {
                const p = PRODUCTS.find((x) => x.id === l.id);
                if (!p) return null;
                const price = salePrice(p, flash);
                return (
                  <li key={l.id} className="flex flex-wrap items-center gap-4 p-4">
                    <Link to="/product/$slug" params={{ slug: p.slug }} className="packshot size-24">
                      <img src={p.image} alt="" />
                    </Link>
                    <div className="min-w-0 flex-1">
                      <Link to="/product/$slug" params={{ slug: p.slug }} className="font-medium text-wine hover:underline">
                        {p.name}
                      </Link>
                      <p className="mt-1 text-sm font-semibold">{qar(price)}</p>
                      <p className="text-xs font-semibold text-wine">{t.inStock}</p>
                      <div className="mt-3 flex flex-wrap items-center gap-3">
                        <QtyStepper value={l.qty} onChange={(n) => setQty(l.id, n)} max={p.stock} />
                        <button type="button" className="text-sm text-wine hover:underline" onClick={() => remove(l.id)}>
                          {t.remove}
                        </button>
                      </div>
                    </div>
                    <p className="w-24 text-end font-semibold">{qar(price * l.qty)}</p>
                  </li>
                );
              })}
            </ul>
            <aside className="h-fit border border-line bg-card p-4 shadow-card">
              <p className="text-lg">
                {t.subtotal} ({count}): <span className="font-semibold">{qar(total)}</span>
              </p>
              <p className="mt-2 text-xs text-muted">{t.deliveryNote}</p>
              <Button asChild variant="gold" className="mt-4 w-full">
                <Link to="/checkout">{t.checkout}</Link>
              </Button>
            </aside>
          </div>
        )}
      </div>
    </Shell>
  );
}
