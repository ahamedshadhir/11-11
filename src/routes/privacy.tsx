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
            ? "لا نخزّن أرقام البطاقات أو رموز الأمان. سكيبكاش يعالج الدفع على صفحته. السلة والمفضلة تُحفظ على جهازك. للدعم: support@1111.qa."
            : "We never store card numbers or CVC codes. SkipCash processes the payment on its own page. Cart and wishlist stay on your device. Questions: support@1111.qa."}
        </p>
      </article>
    </Shell>
  );
}
