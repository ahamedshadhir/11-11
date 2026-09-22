import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { Heart, Truck } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { Shell } from "@/components/layout";
import { ProductCard } from "@/components/product-card";
import { QtyStepper } from "@/components/qty-stepper";
import { Stars } from "@/components/stars";
import { Button } from "@/components/ui/button";
import { PRODUCTS, getProduct } from "@/lib/catalog";
import { COPY } from "@/lib/i18n";
import { flashLive, salePrice, useStore } from "@/lib/store";
import { qar } from "@/lib/utils";

export const Route = createFileRoute("/product/$slug")({
  component: ProductPage,
});

function ProductPage() {
  const { slug } = Route.useParams();
  const p = getProduct(slug);
  const lang = useStore((s) => s.lang);
  const flash = useStore((s) => s.flash);
  const area = useStore((s) => s.area);
  const add = useStore((s) => s.add);
  const toggleWish = useStore((s) => s.toggleWish);
  const wish = useStore((s) => s.wish);
  const t = COPY[lang];
  const nav = useNavigate();
  const [qty, setQty] = useState(1);

  if (!p) {
    return (
      <Shell>
        <div className="mx-auto max-w-lg px-4 py-16 text-center">
          <p className="text-muted">{t.noItems}</p>
          <Button asChild className="mt-6">
            <Link to="/shop">{t.shop}</Link>
          </Button>
        </div>
      </Shell>
    );
  }

  const product = p;
  const price = salePrice(product, flash);
  const onSale = flashLive(flash) && price < product.price;
  const related = PRODUCTS.filter((x) => x.categoryId === product.categoryId && x.id !== product.id).slice(0, 4);
  const reviews = 12 + (product.name.length % 40);

  function addBag() {
    add(product.id, qty);
    toast.success(t.added);
  }

  return (
    <Shell>
      <div className="mx-auto max-w-6xl px-4 py-8">
        <p className="text-sm text-muted">
          <Link to="/" className="hover:text-wine">
            {t.home}
          </Link>
          {" / "}
          <Link to="/shop" search={{ category: product.categoryId }} className="hover:text-wine">
            {t.shop}
          </Link>
          {" / "}
          {product.name}
        </p>
        <div className="mt-6 grid gap-10 lg:grid-cols-2">
          <div className="rounded-xl bg-card p-8 shadow-card">
            <div className="packshot mx-auto h-96">
              <img
                src={product.imageHero}
                alt={product.name}
                width={900}
                height={900}
                decoding="async"
              />
            </div>
          </div>
          <div>
            <h1 className="font-display text-3xl font-semibold text-ink">{product.name}</h1>
            <div className="mt-3">
              <Stars value={product.rating} count={reviews} />
            </div>
            <p className="mt-4 text-lg">
              {onSale ? (
                <>
                  <s className="me-2 text-muted">{qar(product.price)}</s>
                  <span className="font-semibold text-wine">{qar(price)}</span>
                </>
              ) : (
                <span className="font-semibold">{qar(product.price)}</span>
              )}
            </p>
            <p className="mt-4 max-w-prose text-muted">{product.description}</p>
            <p className="mt-4 text-sm text-wine">
              {t.inStock} · {product.stock} {t.left}
            </p>
            <p className="mt-2 flex items-center gap-2 text-sm text-muted">
              <Truck className="size-4" />
              {t.deliverTo} {area}. {t.deliveryNote}
            </p>
            <div className="mt-6 flex flex-wrap items-center gap-3">
              <QtyStepper value={qty} onChange={setQty} max={product.stock} />
              <Button type="button" onClick={addBag}>
                {t.addToCart}
              </Button>
              <Button
                type="button"
                variant="gold"
                onClick={() => {
                  addBag();
                  void nav({ to: "/checkout" });
                }}
              >
                {t.buyNow}
              </Button>
              <Button type="button" variant="outline" onClick={() => toggleWish(product.id)}>
                <Heart className="size-4" fill={wish.includes(product.id) ? "currentColor" : "none"} />
                {t.wishlist}
              </Button>
            </div>
          </div>
        </div>
        {related.length ? (
          <div className="mt-14">
            <h2 className="font-display text-xl font-semibold">{t.related}</h2>
            <div className="mt-4 grid grid-cols-2 gap-4 lg:grid-cols-4">
              {related.map((r) => (
                <ProductCard key={r.id} p={r} />
              ))}
            </div>
          </div>
        ) : null}
      </div>
    </Shell>
  );
}
