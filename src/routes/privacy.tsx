import { createFileRoute } from "@tanstack/react-router";
import { Shell } from "@/components/layout";
import { COPY } from "@/lib/i18n";
import { useStore } from "@/lib/store";

export const Route = createFileRoute("/privacy")({ component: Privacy });

function Privacy() {
  const lang = useStore((s) => s.lang);
  const t = COPY[lang];
  const ar = lang === "ar";
  return (
    <Shell>
      <article className="mx-auto max-w-2xl px-4 py-12">
        <h1 className="font-display text-3xl font-semibold text-wine">{t.privacy}</h1>
        <p className="mt-4 text-muted">
          {ar
            ? "نحتفظ ببيانات الطلب (الاسم، الهاتف، العنوان) لإتمام التوصيل داخل قطر. لا نبيع بياناتك. تسجيل الدخول يحفظ الطلبات في حسابك فقط."
            : "We keep order details (name, phone, address) to deliver in Qatar. We do not sell your data. Signing in stores orders against your account only."}
        </p>
        <p className="mt-3 text-muted">
          {ar
            ? "السلة والمفضلة تُحفظ على جهازك. للدعم: support@1111.qa."
            : "Cart and wishlist stay on your device unless you check out while signed in. Questions: support@1111.qa."}
        </p>
      </article>
    </Shell>
  );
}
