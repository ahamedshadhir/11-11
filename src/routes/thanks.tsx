import { createFileRoute, Link } from "@tanstack/react-router";
import { Shell } from "@/components/layout";
import { Button } from "@/components/ui/button";
import { COPY } from "@/lib/i18n";
import { useStore } from "@/lib/store";
import { qar } from "@/lib/utils";

export const Route = createFileRoute("/thanks")({
  validateSearch: (s: Record<string, unknown>) => ({
    id: typeof s.id === "string" ? s.id : "",
  }),
  component: Thanks,
});

function Thanks() {
  const { id } = Route.useSearch();
  const lang = useStore((s) => s.lang);
  const orders = useStore((s) => s.orders);
  const t = COPY[lang];
  const order = orders.find((o) => o.id === id) ?? orders[0];

  return (
    <Shell>
      <div className="mx-auto max-w-lg px-4 py-16 text-center">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">11-11</p>
        <h1 className="mt-3 font-display text-3xl font-semibold text-wine">{t.orderOk}</h1>
        {order ? (
          <div className="mt-6 rounded-xl bg-card p-6 text-start text-sm shadow-card">
            <p>
              #{order.id} · {order.pay === "cod" ? t.cod : t.skipcash}
            </p>
            <p className="mt-2">
              {order.name} · {order.area}
            </p>
            <p className="mt-1 text-muted">{order.address}</p>
            <p className="mt-4 font-semibold">{qar(order.total)}</p>
            <ul className="mt-3 space-y-1 text-muted">
              {order.lines.map((l) => (
                <li key={l.id}>
                  {l.name} × {l.qty}
                </li>
              ))}
            </ul>
          </div>
        ) : null}
        <div className="mt-8 flex justify-center gap-3">
          <Button asChild>
            <Link to="/shop">{t.continue}</Link>
          </Button>
          <Button asChild variant="outline">
            <Link to="/account">{t.orders}</Link>
          </Button>
        </div>
      </div>
    </Shell>
  );
}
