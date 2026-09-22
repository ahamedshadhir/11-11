import { Link } from "@tanstack/react-router";
import { Heart } from "lucide-react";
import { toast } from "sonner";
import type { Product } from "@/lib/catalog";
import { COPY } from "@/lib/i18n";
import { flashLive, salePrice, useStore } from "@/lib/store";
import { qar } from "@/lib/utils";
import { Button } from "./ui/button";
import { Stars } from "./stars";

export function ProductCard({ p }: { p: Product }) {
  const lang = useStore((s) => s.lang);
  const flash = useStore((s) => s.flash);
  const add = useStore((s) => s.add);
  const wish = useStore((s) => s.wish);
  const toggleWish = useStore((s) => s.toggleWish);
  const t = COPY[lang];
  const price = salePrice(p, flash);
  const onSale = flashLive(flash) && price < p.price;
  const loved = wish.includes(p.id);

  return (
    <article className="group flex flex-col bg-card p-3 shadow-card transition-[box-shadow] duration-150 hover:shadow-card-hover">
      <Link to="/product/$slug" params={{ slug: p.slug }} className="relative block">
        <span className="packshot aspect-square">
          <img
            src={p.image}
            alt={p.name}
            width={400}
            height={400}
            loading="lazy"
            decoding="async"
          />
        </span>
        {onSale ? (
          <span className="absolute start-2 top-2 rounded-sm bg-gold px-1.5 py-0.5 text-xs font-bold text-wine">
            −{flash.discount}%
          </span>
        ) : null}
      </Link>
      <div className="mt-2 flex flex-1 flex-col gap-1">
        <div className="flex items-start justify-between gap-2">
          <h3 className="text-sm font-medium leading-snug text-wine hover:underline">
            <Link to="/product/$slug" params={{ slug: p.slug }}>
              {p.name}
            </Link>
          </h3>
          <button
            type="button"
            aria-label={t.wishlist}
            aria-pressed={loved}
            onClick={() => toggleWish(p.id)}
            className="relative grid size-11 shrink-0 place-items-center text-muted hover:text-wine"
          >
            <Heart className="size-4" fill={loved ? "currentColor" : "none"} />
          </button>
        </div>
        <Stars value={p.rating} />
        <p className="text-lg font-semibold text-fg">
          {onSale ? (
            <>
              <span className="text-wine">{qar(price)}</span>
              <s className="ms-2 text-sm font-normal text-muted">{qar(p.price)}</s>
            </>
          ) : (
            qar(p.price)
          )}
        </p>
        <p className="text-xs font-semibold text-wine">{t.nextDay}</p>
        <p className="text-xs text-muted">{t.prime}</p>
        <Button
          className="mt-auto w-full"
          variant="gold"
          type="button"
          onClick={() => {
            add(p.id);
            toast.success(t.added);
          }}
        >
          {t.addToCart}
        </Button>
      </div>
    </article>
  );
}
