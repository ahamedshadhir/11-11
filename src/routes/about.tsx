import { createFileRoute } from "@tanstack/react-router";
import { Shell } from "@/components/layout";
import { useStore } from "@/lib/store";

export const Route = createFileRoute("/about")({ component: About });

function About() {
  const lang = useStore((s) => s.lang);
  const ar = lang === "ar";
  return (
    <Shell>
      <article className="mx-auto max-w-2xl px-4 py-12">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">11:11</p>
        <h1 className="mt-2 font-display text-4xl font-semibold text-wine">
          {ar ? "من نحن" : "A Doha house for the pieces you actually keep."}
        </h1>
        <p className="mt-6 text-muted">
          {ar
            ? "11-11 متجر قطري للإلكترونيات والأزياء والمنزل. نختار المنتجات بعناية، نعرضها كما هي، ونوصلها داخل قطر — كاش عند الاستلام أو سكيبكاش."
            : "11-11 is a Qatar store for electronics, fashion and home. We photograph products as they are, price them in QAR, and deliver across Doha, Lusail, Al Wakrah and beyond — cash on delivery or SkipCash."}
        </p>
        <p className="mt-4 text-muted">
          {ar
            ? "الاسم 11:11 إشارة للحظة التي تتوقف فيها. نريد أن يكون التسوق واضحاً: صور حقيقية، خصم واضح، ودعم من الدوحة."
            : "The 11:11 lockup is a pause — a moment to choose well. No stock-photo theatre: the phone you tap is the phone on the card. Flash sales are timed. Support sits in Doha."}
        </p>
        <dl className="mt-10 grid gap-6 sm:grid-cols-3">
          <Fact k={ar ? "المقر" : "Based"} v={ar ? "الدوحة، قطر" : "Doha, Qatar"} />
          <Fact k={ar ? "التوصيل" : "Delivery"} v={ar ? "1–3 أيام" : "1–3 days"} />
          <Fact k={ar ? "الدفع" : "Pay"} v="COD · SkipCash" />
        </dl>
      </article>
    </Shell>
  );
}

function Fact({ k, v }: { k: string; v: string }) {
  return (
    <div className="rounded-xl bg-card p-4 shadow-card">
      <dt className="text-xs uppercase tracking-widest text-gold">{k}</dt>
      <dd className="mt-1 font-medium">{v}</dd>
    </div>
  );
}
