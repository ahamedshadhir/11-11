import { createFileRoute } from "@tanstack/react-router";
import { Shell } from "@/components/layout";
import { COPY } from "@/lib/i18n";
import { useStore } from "@/lib/store";

export const Route = createFileRoute("/terms")({ component: Terms });

function Terms() {
  const lang = useStore((s) => s.lang);
  const t = COPY[lang];
  const ar = lang === "ar";
  return (
    <Shell>
      <article className="mx-auto max-w-2xl px-4 py-12">
        <h1 className="font-display text-3xl font-semibold text-wine">{t.terms}</h1>
        <p className="mt-4 text-muted">
          {ar
            ? "الأسعار بالريال القطري. الطلبات تخضع للتوفر. الإرجاع خلال 30 يوماً للمنتجات غير المستخدمة. سكيبكاش بوابة دفع مرخّصة؛ يُحفظ الطلب في قاعدة البيانات قبل الدفع. الدفع عند الاستلام متاح في قطر."
            : "Prices are in Qatari Riyal. Orders are subject to stock. Unused items can be returned within 30 days. SkipCash is a licensed payment gateway; every order is saved to the database before you pay. Cash on delivery is available across Qatar."}
        </p>
      </article>
    </Shell>
  );
}
