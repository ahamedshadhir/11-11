import { createServerFn } from "@tanstack/react-start";
import { authMiddleware } from "@/lib/auth/middleware";
import { getSql } from "@/lib/db";
import type { Order } from "./store";

function parseOrder(payload: unknown): Order {
  const raw = typeof payload === "string" ? JSON.parse(payload) : payload;
  return raw as Order;
}

export const saveOrder = createServerFn({ method: "POST" })
  .middleware([authMiddleware])
  .validator((order: Order) => order)
  .handler(async ({ context, data }) => {
    const sql = await getSql();
    await sql`
      insert into store_orders (id, user_id, payload)
      values (${data.id}, ${context.userId}, ${JSON.stringify(data)})
      on conflict (id) do update set payload = excluded.payload
    `;
    return { ok: true as const };
  });

export const listOrders = createServerFn({ method: "GET" })
  .middleware([authMiddleware])
  .handler(async ({ context }) => {
    const sql = await getSql();
    const rows = await sql<{ payload: unknown }>`
      select payload from store_orders
      where user_id = ${context.userId}
      order by created_at desc
    `;
    return rows.map((r) => parseOrder(r.payload));
  });
