import { createFileRoute, Link, Navigate, useNavigate } from "@tanstack/react-router";
import { FormEvent, useState } from "react";
import { toast } from "sonner";
import { useCurrentUserState } from "@/lib/auth/use-current-user";
import { Shell } from "@/components/layout";
import { Button } from "@/components/ui/button";
import { PRODUCTS, QATAR_AREAS } from "@/lib/catalog";
import { COPY } from "@/lib/i18n";
import { checkoutOrder } from "@/lib/orders";
import { cartTotal, salePrice, useHydrated, useStore, type PayMethod } from "@/lib/store";
import { qar } from "@/lib/utils";

export const Route = createFileRoute("/checkout")({ component: Checkout });

function Checkout() {
  const lang = useStore((s) => s.lang);
  const cart = useStore((s) => s.cart);
  const flash = useStore((s) => s.flash);
  const area = useStore((s) => s.area);
  const rememberOrder = useStore((s) => s.rememberOrder);
  const clearCart = useStore((s) => s.clearCart);
  const t = COPY[lang];
  const nav = useNavigate();
  const { user, isPending } = useCurrentUserState();
  const [pay, setPay] = useState<PayMethod>("cod");
  const [busy, setBusy] = useState(false);
  const ready = useHydrated();
  const total = cartTotal(cart, flash);

  if (isPending || !ready) {
    return (
      <Shell>
        <div className="mx-auto max-w-5xl px-4 py-10">
          <div className="h-64 animate-pulse rounded-xl bg-line" />
        </div>
      </Shell>
    );
  }

  if (!user) {
    return <Navigate to="/login" search={{ next: "/checkout" }} />;
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

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (busy) return;
    const fd = new FormData(e.currentTarget);
    setBusy(true);
    try {
      const result = await checkoutOrder({
        data: {
          name: String(fd.get("name") || ""),
          phone: String(fd.get("phone") || ""),
          email: String(fd.get("email") || user?.primaryEmail || ""),
          area: String(fd.get("area") || area),
          address: String(fd.get("address") || ""),
          pay,
          lines: cart.map((l) => ({ id: l.id, qty: l.qty })),
        },
      });
      rememberOrder(result.order);
      clearCart();
      if (result.warning) toast.message(result.warning);
      if (result.mode === "skipcash" && result.payUrl) {
        window.location.assign(result.payUrl);
        return;
      }
      if (result.mode === "hosted") {
        await nav({ to: "/pay/skipcash", search: { id: result.order.id } });
        return;
      }
      await nav({ to: "/thanks", search: { id: result.order.id } });
    } catch (err) {
      setBusy(false);
      toast.error(err instanceof Error && err.message ? err.message : t.orderSaveFailed);
    }
  }

  return (
    <Shell>
      <form onSubmit={onSubmit} className="mx-auto grid max-w-5xl gap-6 px-4 py-10 lg:grid-cols-2">
        <section className="rounded-xl bg-card p-6 shadow-card">
          <h1 className="font-display text-2xl font-semibold text-wine">{t.checkout}</h1>
          <p className="mt-2 text-sm text-muted">{t.signedInCheckout}</p>
          <div className="mt-4 grid gap-3">
            <label className="text-sm">
              {t.name}
              <input required name="name" defaultValue={user.displayName ?? ""} className="field mt-1" />
            </label>
            <label className="text-sm">
              {t.email}
              <input
                required
                name="email"
                type="email"
                defaultValue={user.primaryEmail ?? ""}
                className="field mt-1"
              />
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
          <Button className="mt-6 w-full" variant="gold" type="submit" disabled={busy}>
            {busy ? t.savingOrder : pay === "skipcash" ? t.skipcashPay : t.placeOrder}
          </Button>
        </section>
      </form>
    </Shell>
  );
}
