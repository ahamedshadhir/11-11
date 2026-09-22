import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { FormEvent, useState } from "react";
import { Shell } from "@/components/layout";
import { Button } from "@/components/ui/button";
import { PRODUCTS, QATAR_AREAS } from "@/lib/catalog";
import { COPY } from "@/lib/i18n";
import { saveOrder } from "@/lib/orders";
import { cartTotal, salePrice, useHydrated, useStore, type PayMethod } from "@/lib/store";
import { qar } from "@/lib/utils";

export const Route = createFileRoute("/checkout")({ component: Checkout });

function Checkout() {
  const lang = useStore((s) => s.lang);
  const cart = useStore((s) => s.cart);
  const flash = useStore((s) => s.flash);
  const area = useStore((s) => s.area);
  const placeOrder = useStore((s) => s.placeOrder);
  const t = COPY[lang];
  const nav = useNavigate();
  const [pay, setPay] = useState<PayMethod>("cod");
  const [sheet, setSheet] = useState(false);
  const [busy, setBusy] = useState(false);
  const ready = useHydrated();
  const total = cartTotal(cart, flash);

  if (!ready) {
    return (
      <Shell>
        <div className="mx-auto max-w-5xl px-4 py-10">
          <div className="h-64 animate-pulse rounded-xl bg-line" />
        </div>
      </Shell>
    );
  }

  if (cart.length === 0) {
    return (
      <Shell>
        <p className="p-10">
          {t.emptyCart}.{" "}
          <Link to="/shop" className="text-wine underline">
            {t.shop}
          </Link>
        </p>
      </Shell>
    );
  }

  function buildOrder(fd: FormData) {
    const lines = cart
      .map((l) => {
        const p = PRODUCTS.find((x) => x.id === l.id);
        if (!p) return null;
        return { id: p.id, name: p.name, qty: l.qty, price: salePrice(p, flash) };
      })
      .filter((x): x is NonNullable<typeof x> => Boolean(x));
    return placeOrder({
      name: String(fd.get("name") || ""),
      phone: String(fd.get("phone") || ""),
      area: String(fd.get("area") || area),
      address: String(fd.get("address") || ""),
      pay,
      total,
      lines,
    });
  }

  async function persist(order: ReturnType<typeof placeOrder>) {
    try {
      await saveOrder({ data: order });
    } catch {
      /* guest checkout still succeeds locally */
    }
    void nav({ to: "/thanks", search: { id: order.id } });
  }

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (pay === "skipcash") {
      setSheet(true);
      return;
    }
    const order = buildOrder(new FormData(e.currentTarget));
    await persist(order);
  }

  async function authorizeSkip() {
    const form = document.getElementById("checkout-form") as HTMLFormElement | null;
    if (!form) return;
    setBusy(true);
    await new Promise((r) => setTimeout(r, 1100));
    const order = buildOrder(new FormData(form));
    await persist(order);
  }

  return (
    <Shell>
      <form id="checkout-form" onSubmit={onSubmit} className="mx-auto grid max-w-5xl gap-6 px-4 py-10 lg:grid-cols-2">
        <section className="rounded-xl bg-card p-6 shadow-card">
          <h1 className="font-display text-2xl font-semibold text-wine">{t.checkout}</h1>
          <p className="mt-2 text-sm text-muted">{t.guest}</p>
          <div className="mt-4 grid gap-3">
            <label className="text-sm">
              {t.name}
              <input required name="name" className="field mt-1" />
            </label>
            <label className="text-sm">
              {t.phone}
              <input required name="phone" inputMode="tel" className="field mt-1" placeholder="+974" />
            </label>
            <label className="text-sm">
              {t.area}
              <select name="area" defaultValue={area} className="field mt-1">
                {QATAR_AREAS.map((a) => (
                  <option key={a}>{a}</option>
                ))}
              </select>
            </label>
            <label className="text-sm">
              {t.address}
              <input required name="address" className="field mt-1" />
            </label>
          </div>
          <h2 className="mt-6 text-sm font-semibold">{t.payment}</h2>
          <div className="mt-2 grid gap-2">
            <label className="flex min-h-11 cursor-pointer items-center gap-3 rounded-md border border-line px-3">
              <input type="radio" checked={pay === "cod"} onChange={() => setPay("cod")} />
              <span>
                <span className="block font-medium">{t.cod}</span>
                <span className="text-xs text-muted">{t.payCodHint}</span>
              </span>
            </label>
            <label className="flex min-h-11 cursor-pointer items-center gap-3 rounded-md border border-line px-3">
              <input type="radio" checked={pay === "skipcash"} onChange={() => setPay("skipcash")} />
              <span>
                <span className="block font-medium">{t.skipcash}</span>
                <span className="text-xs text-muted">{t.paySkipHint}</span>
              </span>
            </label>
          </div>
        </section>
        <section className="rounded-xl bg-card p-6 shadow-card">
          <h2 className="font-semibold">{t.cart}</h2>
          <ul className="mt-3 space-y-2 text-sm">
            {cart.map((l) => {
              const p = PRODUCTS.find((x) => x.id === l.id);
              if (!p) return null;
              return (
                <li key={l.id} className="flex justify-between gap-3">
                  <span>
                    {p.name} × {l.qty}
                  </span>
                  <span>{qar(salePrice(p, flash) * l.qty)}</span>
                </li>
              );
            })}
          </ul>
          <p className="mt-4 text-lg font-semibold">
            {t.total}: {qar(total)}
          </p>
          <Button className="mt-6 w-full" variant="gold" type="submit">
            {pay === "skipcash" ? t.skipcashPay : t.placeOrder}
          </Button>
        </section>
      </form>
      {sheet ? (
        <div className="fixed inset-0 z-50 grid place-items-center bg-ink/50 p-4">
          <div className="w-full max-w-sm rounded-xl bg-card p-6 shadow-pop">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">SkipCash</p>
            <h2 className="mt-2 font-display text-2xl text-wine">{t.skipcashPay}</h2>
            <p className="mt-2 text-sm text-muted">{qar(total)} · 11-11 Doha</p>
            <div className="mt-6 rounded-md bg-cream p-4 text-sm">
              <p className="font-medium">{t.authorize}</p>
              <p className="mt-1 text-muted">{t.paySkipHint}</p>
            </div>
            <div className="mt-6 flex gap-2">
              <Button className="flex-1" type="button" disabled={busy} onClick={() => void authorizeSkip()}>
                {busy ? t.paying : t.authorize}
              </Button>
              <Button variant="outline" type="button" disabled={busy} onClick={() => setSheet(false)}>
                {t.cancel}
              </Button>
            </div>
          </div>
        </div>
      ) : null}
    </Shell>
  );
}
