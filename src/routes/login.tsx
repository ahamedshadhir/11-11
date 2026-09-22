import { createFileRoute, Link } from "@tanstack/react-router";
import { FormEvent, useState } from "react";
import { GROK_PROVIDERS, authClient, authEnabled, signIn } from "@/lib/auth/client";
import { Logo } from "@/components/logo";
import { Button } from "@/components/ui/button";
import { COPY } from "@/lib/i18n";
import { useStore } from "@/lib/store";

export const Route = createFileRoute("/login")({ component: Login });

function Login() {
  const lang = useStore((s) => s.lang);
  const t = COPY[lang];
  const [mode, setMode] = useState<"in" | "up">("in");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  async function onEmail(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setErr("");
    setBusy(true);
    const fd = new FormData(e.currentTarget);
    const email = String(fd.get("email") || "");
    const password = String(fd.get("password") || "");
    const name = String(fd.get("name") || "11-11 member");
    try {
      if (mode === "up") {
        const r = await authClient.signUp.email({ email, password, name, callbackURL: "/" });
        if (r.error) throw new Error(r.error.message);
      } else {
        const r = await authClient.signIn.email({ email, password, callbackURL: "/" });
        if (r.error) throw new Error(r.error.message);
      }
      window.location.href = "/";
    } catch (ex) {
      setBusy(false);
      setErr(ex instanceof Error ? ex.message : "Could not sign in");
    }
  }

  return (
    <main
      className="grid min-h-screen place-items-center bg-cream px-4 py-10"
      dir={lang === "ar" ? "rtl" : "ltr"}
    >
      <div className="w-full max-w-sm rounded-xl bg-card p-8 shadow-card">
        <Logo />
        <h1 className="mt-6 text-center font-display text-2xl font-semibold text-wine">
          {mode === "in" ? t.login : t.create}
        </h1>
        {authEnabled ? (
          <div className="mt-6 space-y-2">
            {GROK_PROVIDERS.map((p) => (
              <button
                key={p.providerId}
                type="button"
                onClick={() => signIn(p.providerId, { callbackURL: "/" })}
                className="h-11 w-full rounded-md border border-line text-sm font-medium hover:bg-cream"
              >
                Continue with {p.label}
              </button>
            ))}
          </div>
        ) : (
          <p className="mt-4 text-sm text-muted">Sign-in is disabled.</p>
        )}
        <div className="my-6 flex items-center gap-3 text-xs uppercase tracking-widest text-muted">
          <span className="h-px flex-1 bg-line" />
          or
          <span className="h-px flex-1 bg-line" />
        </div>
        <form onSubmit={onEmail} className="grid gap-3">
          {mode === "up" ? (
            <input name="name" placeholder={t.name} className="field" />
          ) : null}
          <input required name="email" type="email" placeholder={t.email} className="field" />
          <input
            required
            name="password"
            type="password"
            minLength={8}
            placeholder={t.password}
            className="field"
          />
          {err ? <p className="text-sm text-wine">{err}</p> : null}
          <Button type="submit" disabled={busy}>
            {mode === "in" ? t.login : t.create}
          </Button>
        </form>
        <button
          type="button"
          className="mt-4 w-full text-center text-sm text-muted"
          onClick={() => setMode(mode === "in" ? "up" : "in")}
        >
          {mode === "in" ? t.create : t.login}
        </button>
        <p className="mt-6 text-center text-sm">
          <Link to="/" className="text-wine">
            {t.continue}
          </Link>
        </p>
      </div>
    </main>
  );
}
