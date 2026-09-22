import { createFileRoute, Link } from "@tanstack/react-router";
import { ShoppingBag } from "lucide-react";
import { Shell } from "@/components/layout";
import { QtyStepper } from "@/components/qty-stepper";
import { Button } from "@/components/ui/button";
import { PRODUCTS } from "@/lib/catalog";
import { COPY } from "@/lib/i18n";
import { cartTotal, salePrice, useHydrated, useStore } from "@/lib/store";
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

  return (
    <Shell>
      <div className="mx-auto max-w-3xl px-4 py-10">
        <h1 className="font-display text-3xl font-semibold text-wine">{t.cart}</h1>
        {!ready ? (
          <div className="mt-6 h-40 animate-pulse rounded-xl bg-line" />
        ) : cart.length === 0 ? (
          <div className="mt-10 rounded-xl bg-card px-6 py-16 text-center shadow-card">
            <ShoppingBag className="mx-auto size-10 text-gold" />
            <p className="mt-4 text-muted">{t.emptyCart}</p>
            <Button asChild className="mt-6">
              <Link to="/shop">{t.shop}</Link>
            </Button>
          </div>
        ) : (
          <ul className="mt-6 divide-y divide-line rounded-xl bg-card shadow-card">
            {cart.map((l) => {
              const p = PRODUCTS.find((x) => x.id === l.id);
              if (!p) return null;
              const price = salePrice(p, flash);
              return (
                <li key={l.id} className="flex flex-wrap items-center gap-4 p-4">
                  <Link to="/product/$slug" params={{ slug: p.slug }} className="packshot size-16">
                    <img src={p.image} alt="" />
                  </Link>
                  <div className="min-w-0 flex-1">
                    <Link to="/product/$slug" params={{ slug: p.slug }} className="font-medium">
                      {p.name}
                    </Link>
                    <p className="text-sm text-muted">{qar(price)}</p>
                  </div>
                  <QtyStepper value={l.qty} onChange={(n) => setQty(l.id, n)} max={p.stock} />
                  <p className="w-24 text-end font-semibold">{qar(price * l.qty)}</p>
                  <button type="button" className="text-sm text-muted hover:text-wine" onClick={() => remove(l.id)}>
                    {t.remove}
                  </button>
                </li>
              );
            })}
          </ul>
        )}
        {cart.length ? (
          <div className="mt-6 flex flex-wrap items-center justify-between gap-4">
            <p className="text-lg font-semibold">
              {t.total}: {qar(total)}
            </p>
            <Button asChild>
              <Link to="/checkout">{t.checkout}</Link>
            </Button>
          </div>
        ) : null}
      </div>
    </Shell>
  );
}
