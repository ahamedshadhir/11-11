import { Link } from "@tanstack/react-router";
import { cn } from "@/lib/utils";

export function Logo({
  className,
  to = "/",
  invert = false,
  compact = false,
}: {
  className?: string;
  to?: string;
  invert?: boolean;
  compact?: boolean;
}) {
  return (
    <Link
      to={to}
      className={cn("flex flex-col items-center leading-none no-underline", className)}
      aria-label="11:11 eleven-eleven"
    >
      <span
        className={cn(
          "font-display font-semibold tracking-tight",
          compact ? "text-2xl" : "text-3xl",
          invert ? "text-cream" : "text-wine",
        )}
      >
        11<span className="text-gold">:</span>11
      </span>
      <span className="logo-word">eleven-eleven</span>
    </Link>
  );
}
