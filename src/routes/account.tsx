import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useMemo, useState } from "react";
import { RedirectToSignIn, UserButton } from "@/lib/auth/gates";
import { useCurrentUserState } from "@/lib/auth/use-current-user";
import { Shell } from "@/components/layout";
import { Button } from "@/components/ui/button";
import { COPY } from "@/lib/i18n";
import { listOrders } from "@/lib/orders";
import { useStore, type Order } from "@/lib/store";
import { qar } from "@/lib/utils";

export const Route = createFileRoute("/account")({ component: Account });

function Account() {
  const { user, isPending } = useCurrentUserState();
  const lang = useStore((s) => s.lang);
  const local = useStore((s) => s.orders);
  const t = COPY[lang];
  const [remote, setRemote] = useState<Order[]>([]);

  useEffect(() => {
    if (!user) return;
    void listOrders()
      .then(setRemote)
      .catch(() => setRemote([]));
  }, [user]);

  const orders = useMemo(() => {
    const map = new Map<string, Order>();
    for (const o of [...remote, ...local]) map.set(o.id, o);
    return [...map.values()].sort((a, b) => b.at - a.at);
  }, [remote, local]);

  if (isPending) {
    return (
      <Shell>
        <div className="mx-auto max-w-3xl px-4 py-16">
          <div className="h-8 w-40 animate-pulse rounded-md bg-line" />
          <div className="mt-6 h-40 animate-pulse rounded-xl bg-line" />
        </div>
      </Shell>
    );
  }
  if (!user) return <RedirectToSignIn />;

  return (
    <Shell>
      <div className="mx-auto max-w-3xl px-4 py-10">
        <h1 className="font-display text-3xl font-semibold text-wine">{t.account}</h1>
        <section className="mt-6 rounded-xl bg-card p-6 shadow-card">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">{t.profile}</p>
          <p className="mt-2 text-lg font-medium">{user.displayName ?? t.account}</p>
          <p className="text-sm text-muted">{user.primaryEmail}</p>
          <div className="mt-4">
            <UserButton />
          </div>
        </section>
        <div className="mt-8 flex items-end justify-between">
          <h2 className="font-display text-xl font-semibold">{t.orders}</h2>
          <Link to="/wishlist" className="text-sm text-gold">
            {t.wishlist}
          </Link>
        </div>
        {orders.length === 0 ? (
          <div className="mt-4 rounded-xl bg-card p-8 text-center shadow-card">
            <p className="text-muted">{t.noOrders}</p>
            <Button asChild className="mt-4">
              <Link to="/shop">{t.shop}</Link>
            </Button>
          </div>
        ) : (
          <ul className="mt-4 space-y-3">
            {orders.map((o) => (
              <li key={o.id} className="rounded-xl bg-card p-4 shadow-card">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="font-medium">#{o.id}</p>
                  <p className="text-sm text-muted">{new Date(o.at).toLocaleString()}</p>
                </div>
                <p className="mt-1 text-sm">
                  {o.pay === "cod" ? t.cod : t.skipcash} · {o.area}
                </p>
                <ul className="mt-2 text-sm text-muted">
                  {o.lines.map((l) => (
                    <li key={l.id}>
                      {l.name} × {l.qty}
                    </li>
                  ))}
                </ul>
                <p className="mt-2 font-semibold">{qar(o.total)}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </Shell>
  );
}
