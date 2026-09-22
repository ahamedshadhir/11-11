import { useEffect, useState } from "react";
import { COPY } from "@/lib/i18n";
import { useStore } from "@/lib/store";

function pad(n: number) {
  return String(n).padStart(2, "0");
}

export function Countdown({ endsAt }: { endsAt: number }) {
  const lang = useStore((s) => s.lang);
  const t = COPY[lang];
  const [now, setNow] = useState<number | null>(null);

  useEffect(() => {
    setNow(Date.now());
    const id = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);

  const left = now === null ? 0 : Math.max(0, endsAt - now);
  const h = Math.floor(left / 3_600_000);
  const m = Math.floor((left % 3_600_000) / 60_000);
  const s = Math.floor((left % 60_000) / 1000);

  return (
    <div className="flex items-end gap-2" aria-live="polite">
      <Box n={now === null ? "--" : pad(h)} label={t.hours} />
      <span className="mb-2 font-display text-xl text-wine">:</span>
      <Box n={now === null ? "--" : pad(m)} label={t.minutes} />
      <span className="mb-2 font-display text-xl text-wine">:</span>
      <Box n={now === null ? "--" : pad(s)} label={t.seconds} />
    </div>
  );
}

function Box({ n, label }: { n: string; label: string }) {
  return (
    <div className="grid min-w-14 place-items-center rounded-md bg-wine px-3 py-2 text-cream">
      <span className="font-display text-xl leading-none tabular-nums">{n}</span>
      <span className="mt-1 text-[0.6rem] uppercase tracking-wider text-gold">{label}</span>
    </div>
  );
}
