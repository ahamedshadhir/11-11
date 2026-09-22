import { createFileRoute } from "@tanstack/react-router";
import { FormEvent, useState } from "react";
import { toast } from "sonner";
import { Shell } from "@/components/layout";
import { Button } from "@/components/ui/button";
import { COPY } from "@/lib/i18n";
import { useStore } from "@/lib/store";

export const Route = createFileRoute("/contact")({ component: Contact });

function Contact() {
  const lang = useStore((s) => s.lang);
  const t = COPY[lang];
  const [sent, setSent] = useState(false);

  function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSent(true);
    toast.success(t.sent);
    e.currentTarget.reset();
  }

  return (
    <Shell>
      <div className="mx-auto grid max-w-4xl gap-8 px-4 py-12 lg:grid-cols-2">
        <div>
          <h1 className="font-display text-3xl font-semibold text-wine">{t.contact}</h1>
          <p className="mt-3 text-muted">Doha, Qatar · support@1111.qa</p>
          <p className="mt-2 text-sm text-muted">{t.deliveryNote}</p>
        </div>
        <form onSubmit={onSubmit} className="rounded-xl bg-card p-6 shadow-card">
          <label className="text-sm">
            {t.name}
            <input required name="name" className="field mt-1" />
          </label>
          <label className="mt-3 block text-sm">
            {t.email}
            <input required type="email" name="email" className="field mt-1" />
          </label>
          <label className="mt-3 block text-sm">
            {t.message}
            <textarea required name="message" rows={5} className="field mt-1" />
          </label>
          <Button className="mt-4 w-full" type="submit">
            {sent ? t.sent : t.send}
          </Button>
        </form>
      </div>
    </Shell>
  );
}
