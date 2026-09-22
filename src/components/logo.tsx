import { Link } from "@tanstack/react-router";
import { cn } from "@/lib/utils";

export function Logo({
  className,
  to = "/",
  invert = false,
}: {
  className?: string;
  to?: string;
  invert?: boolean;
}) {
  return (
    <Link
      to={to}
      className={cn("flex flex-col items-center leading-none no-underline", className)}
      aria-label="11:11 eleven-eleven"
    >
      <span
        className={cn(
          "font-display text-[1.85rem] font-semibold tracking-tight",
          invert ? "text-cream" : "text-wine",
        )}
      >
        11<span className="text-gold">:</span>11
      </span>
      <span className="mt-1 text-[0.5rem] font-semibold tracking-[0.22em] text-gold">
        eleven-eleven
      </span>
    </Link>
  );
}
