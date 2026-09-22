import { createFileRoute, Link } from "@tanstack/react-router";
import { FormEvent, useEffect, useMemo, useState } from "react";
import { toast } from "sonner";
import { RedirectToSignIn } from "@/lib/auth/gates";
import { useCurrentUserState } from "@/lib/auth/use-current-user";
import { isAdminEmail } from "@/lib/admin";
import { Shell } from "@/components/layout";
import { Button } from "@/components/ui/button";
import { CATEGORIES, PRODUCTS } from "@/lib/catalog";
import { COPY } from "@/lib/i18n";
import { flashLive, useStore, type FlashSale } from "@/lib/store";
import { qar } from "@/lib/utils";

export const Route = createFileRoute("/admin")({ component: Admin });

type Tab = "overview" | "flash" | "catalog" | "orders";

function Admin() {
  const { user, isPending } = useCurrentUserState();
  const lang = useStore((s) => s.lang);
  const flash = useStore((s) => s.flash);
  const setFlash = useStore((s) => s.setFlash);
  const orders = useStore((s) => s.orders);
  const t = COPY[lang];
  const [tab, setTab] = useState<Tab>("overview");
  const [draft, setDraft] = useState<FlashSale>(flash);
  const [q, setQ] = useState("");

  useEffect(() => {
    setDraft(flash);
  }, [flash]);

  const live = flashLive(flash);
  const revenue = orders.reduce((n, o) => n + o.total, 0);
  const catalog = useMemo(() => {
    const s = q.trim().toLowerCase();
    if (!s) return PRODUCTS;
    return PRODUCTS.filter((p) => p.name.toLowerCase().includes(s));
  }, [q]);

  if (isPending) {
    return (
      <Shell>
        <div className="mx-auto max-w-6xl px-4 py-16">
          <div className="h-10 w-48 animate-pulse rounded-md bg-line" />
        </div>
      </Shell>
    );
  }
  if (!user) return <RedirectToSignIn />;
  if (!isAdminEmail(user.primaryEmail)) {
    return (
      <Shell>
        <div className="mx-auto max-w-md px-4 py-16 text-center">
          <h1 className="font-display text-2xl font-semibold text-wine">{t.admin}</h1>
          <p className="mt-2 text-sm text-muted">
            {lang === "ar" ? "هذا الحساب ليس مدير المتجر." : "This account is not the store admin."}
          </p>
          <Button asChild className="mt-6">
            <Link to="/login">{t.login}</Link>
          </Button>
        </div>
      </Shell>
    );
  }


  function onSave(e: FormEvent) {
    e.preventDefault();
    const next = {
      ...draft,
      discount: Math.min(80, Math.max(5, Number(draft.discount) || 20)),
      endsAt: new Date(draft.endsAt).valueOf() || Date.now() + 3_600_000,
    };
    setFlash(next);
    setDraft(next);
    toast.success(t.saved);
  }

  function toggleProduct(id: string) {
    const productIds = draft.productIds.includes(id)
      ? draft.productIds.filter((x) => x !== id)
      : [...draft.productIds, id];
    setDraft({ ...draft, productIds });
  }

  const tabs: { id: Tab; label: string }[] = [
    { id: "overview", label: t.overview },
    { id: "flash", label: t.flash },
    { id: "catalog", label: t.catalog },
    { id: "orders", label: t.orders },
  ];

  return (
    <Shell>
      <div className="mx-auto max-w-6xl px-4 py-10">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">11-11</p>
        <h1 className="mt-1 font-display text-3xl font-semibold text-wine">{t.admin}</h1>
        <p className="mt-1 text-sm text-muted">
          {t.signedInAs} {user.displayName ?? user.primaryEmail}
        </p>
        <div className="mt-6 flex gap-2 overflow-x-auto">
          {tabs.map((tabItem) => (
            <button
              key={tabItem.id}
              type="button"
              onClick={() => setTab(tabItem.id)}
              className={`h-11 rounded-full px-4 text-sm font-medium ${
                tab === tabItem.id ? "bg-wine text-cream" : "bg-card text-fg shadow-card"
              }`}
            >
              {tabItem.label}
            </button>
          ))}
        </div>

        {tab === "overview" ? (
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Stat label={t.catalog} value={String(PRODUCTS.length)} />
            <Stat label={t.flash} value={live ? `${flash.discount}%` : "—"} />
            <Stat label={t.orders} value={String(orders.length)} />
            <Stat label={t.total} value={qar(revenue)} />
          </div>
        ) : null}

        {tab === "flash" ? (
          <form onSubmit={onSave} className="mt-8 grid gap-6 lg:grid-cols-[280px_1fr]">
            <div className="rounded-xl bg-card p-5 shadow-card">
              <label className="text-sm">
                {t.title}
                <input
                  className="field mt-1"
                  value={draft.title}
                  onChange={(e) => setDraft({ ...draft, title: e.target.value })}
                />
              </label>
              <label className="mt-3 block text-sm">
                {t.discount}
                <input
                  type="number"
                  min={5}
                  max={80}
                  className="field mt-1"
                  value={draft.discount}
                  onChange={(e) => setDraft({ ...draft, discount: Number(e.target.value) })}
                />
              </label>
              <label className="mt-3 block text-sm">
                {t.ends}
                <input
                  type="datetime-local"
                  className="field mt-1"
                  value={toLocal(draft.endsAt)}
                  onChange={(e) => setDraft({ ...draft, endsAt: new Date(e.target.value).getTime() })}
                />
              </label>
              <label className="mt-4 flex min-h-11 items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={draft.active}
                  onChange={(e) => setDraft({ ...draft, active: e.target.checked })}
                />
                {t.active}
              </label>
              <Button className="mt-4 w-full" type="submit">
                {t.save}
              </Button>
            </div>
            <div>
              <p className="text-sm text-muted">
                {t.select} · {draft.productIds.length}
              </p>
              <div className="mt-3 grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-4">
                {PRODUCTS.map((p) => {
                  const on = draft.productIds.includes(p.id);
                  return (
                    <button
                      key={p.id}
                      type="button"
                      onClick={() => toggleProduct(p.id)}
                      className={`rounded-lg bg-card p-3 text-start shadow-card ${on ? "ring-2 ring-gold" : ""}`}
                    >
                      <span className="packshot h-24">
                        <img src={p.image} alt="" />
                      </span>
                      <span className="mt-2 block text-xs font-medium">{p.name}</span>
                      <span className="text-xs text-muted">{qar(p.price)}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          </form>
        ) : null}

        {tab === "catalog" ? (
          <div className="mt-8">
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder={t.search}
              className="field max-w-sm"
            />
            <div className="mt-4 overflow-x-auto rounded-xl bg-card shadow-card">
              <table className="w-full min-w-[640px] text-start text-sm">
                <thead className="border-b border-line text-xs uppercase tracking-wider text-muted">
                  <tr>
                    <th className="px-4 py-3 font-medium">SKU</th>
                    <th className="px-4 py-3 font-medium">{t.catalog}</th>
                    <th className="px-4 py-3 font-medium">{t.categories}</th>
                    <th className="px-4 py-3 font-medium">{t.total}</th>
                    <th className="px-4 py-3 font-medium">{t.left}</th>
                  </tr>
                </thead>
                <tbody>
                  {catalog.map((p) => (
                    <tr key={p.id} className="border-b border-line last:border-0">
                      <td className="px-4 py-3 font-mono text-xs">{p.id}</td>
                      <td className="px-4 py-3">
                        <span className="flex items-center gap-3">
                          <img src={p.image} alt="" className="size-10 object-contain" />
                          {p.name}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        {CATEGORIES.find((c) => c.id === p.categoryId)?.name}
                      </td>
                      <td className="px-4 py-3">{qar(p.price)}</td>
                      <td className="px-4 py-3">{p.stock}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ) : null}

        {tab === "orders" ? (
          <div className="mt-8 space-y-3">
            {orders.length === 0 ? <p className="text-muted">{t.noOrders}</p> : null}
            {orders.map((o) => (
              <article key={o.id} className="rounded-xl bg-card p-4 shadow-card">
                <div className="flex flex-wrap justify-between gap-2">
                  <p className="font-medium">#{o.id}</p>
                  <p className="text-sm text-muted">{new Date(o.at).toLocaleString()}</p>
                </div>
                <p className="mt-1 text-sm">
                  {o.name} · {o.phone} · {o.area}
                </p>
                <p className="text-sm text-muted">{o.address}</p>
                <p className="mt-2 text-sm">
                  {o.pay === "cod" ? t.cod : t.skipcash} · {qar(o.total)}
                </p>
              </article>
            ))}
          </div>
        ) : null}
      </div>
    </Shell>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl bg-card p-5 shadow-card">
      <p className="text-xs uppercase tracking-widest text-gold">{label}</p>
      <p className="mt-2 font-display text-2xl text-wine">{value}</p>
    </div>
  );
}

function toLocal(ms: number) {
  const d = new Date(ms);
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}
