import { Link } from "@tanstack/react-router";
import { useEffect, useState, type ReactNode } from "react";
import { ClipboardList, LayoutDashboard, LogOut, Menu, Package, Store, Tag, X } from "lucide-react";
import { authEnabled, signOut } from "@/lib/auth/client";
import { COPY } from "@/lib/i18n";
import { useStore } from "@/lib/store";
import { Logo } from "./logo";

export type AdminTab = "overview" | "flash" | "catalog" | "orders";

export function AdminShell({
  children,
  tab,
  onTab,
  userLabel,
}: {
  children: ReactNode;
  tab?: AdminTab;
  onTab?: (tab: AdminTab) => void;
  userLabel?: string;
}) {
  const lang = useStore((s) => s.lang);
  const setLang = useStore((s) => s.setLang);
  const t = COPY[lang];
  const [open, setOpen] = useState(false);
  const [signingOut, setSigningOut] = useState(false);

  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
  }, [lang]);

  const items: { id: AdminTab; label: string; icon: typeof LayoutDashboard }[] = [
    { id: "overview", label: t.overview, icon: LayoutDashboard },
    { id: "flash", label: t.flash, icon: Tag },
    { id: "catalog", label: t.catalog, icon: Package },
    { id: "orders", label: t.orders, icon: ClipboardList },
  ];

  function Nav() {
    return (
      <>
        <Logo invert compact to="/admin" className="px-2 py-4" />
        <p className="px-4 text-xs font-semibold uppercase tracking-widest text-gold">{t.console}</p>
        <nav className="mt-4 flex flex-1 flex-col gap-1 px-2">
          {onTab
            ? items.map((item) => {
                const Icon = item.icon;
                const active = tab === item.id;
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => {
                      onTab(item.id);
                      setOpen(false);
                    }}
                    className={`flex min-h-11 items-center gap-3 rounded-md px-3 text-sm font-medium ${
                      active ? "bg-gold text-wine" : "text-cream hover:bg-cream/10"
                    }`}
                  >
                    <Icon className="size-4" />
                    {item.label}
                  </button>
                );
              })
            : null}
        </nav>
        <div className="mt-auto space-y-1 border-t border-cream/10 p-2">
          <Link
            to="/"
            className="flex min-h-11 items-center gap-3 rounded-md px-3 text-sm text-cream hover:bg-cream/10"
          >
            <Store className="size-4" />
            {t.visitStore}
          </Link>
          {authEnabled ? (
            <button
              type="button"
              disabled={signingOut}
              onClick={() => {
                setSigningOut(true);
                void signOut().catch(() => setSigningOut(false));
              }}
              className="flex min-h-11 w-full items-center gap-3 rounded-md px-3 text-sm text-cream hover:bg-cream/10"
            >
              <LogOut className="size-4" />
              {signingOut ? "…" : t.signOut}
            </button>
          ) : null}
        </div>
      </>
    );
  }

  return (
    <div className="min-h-screen bg-cream text-fg" dir={lang === "ar" ? "rtl" : "ltr"} lang={lang}>
      <div className="flex min-h-screen">
        <aside className="hidden w-60 shrink-0 flex-col bg-wine text-cream lg:flex">
          <Nav />
        </aside>
        {open ? (
          <div className="fixed inset-0 z-50 lg:hidden">
            <button type="button" className="absolute inset-0 bg-ink/50" aria-label={t.cancel} onClick={() => setOpen(false)} />
            <aside className="relative flex h-full w-60 flex-col bg-wine text-cream">
              <button type="button" className="absolute end-2 top-2 grid size-11 place-items-center text-cream" onClick={() => setOpen(false)} aria-label={t.cancel}>
                <X className="size-5" />
              </button>
              <Nav />
            </aside>
          </div>
        ) : null}
        <div className="flex min-w-0 flex-1 flex-col">
          <header className="flex h-14 items-center gap-3 border-b border-line bg-card px-4">
            <button
              type="button"
              className="grid size-11 place-items-center text-wine lg:hidden"
              onClick={() => setOpen(true)}
              aria-label={t.admin}
            >
              <Menu className="size-5" />
            </button>
            <p className="text-sm font-semibold text-wine">{t.admin}</p>
            <div className="ms-auto flex items-center gap-3 text-sm">
              <div className="flex items-center gap-1 text-xs font-semibold" role="group" aria-label="Language">
                <button type="button" onClick={() => setLang("en")} className={lang === "en" ? "text-wine" : "text-muted"}>
                  EN
                </button>
                <span className="text-line">/</span>
                <button type="button" onClick={() => setLang("ar")} className={lang === "ar" ? "text-wine" : "text-muted"}>
                  AR
                </button>
              </div>
              {userLabel ? <span className="hidden text-muted sm:inline">{userLabel}</span> : null}
            </div>
          </header>
          <div className="flex-1 p-4 sm:p-6">{children}</div>
        </div>
      </div>
    </div>
  );
}
