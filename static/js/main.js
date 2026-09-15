(function () {
  const money = (n) => "QAR " + Number(n || 0).toLocaleString(undefined, { maximumFractionDigits: 0 });

  function toast(msg) {
    const wrap = document.getElementById("toasts");
    if (!wrap || !msg) return;
    const el = document.createElement("div");
    el.className = "toast";
    el.textContent = msg;
    wrap.appendChild(el);
    setTimeout(() => el.remove(), 2600);
  }

  function post(url, body) {
    return fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Requested-With": "fetch" },
      body: JSON.stringify(body || {}),
    }).then((r) => r.json());
  }

  function paintCart(data) {
    if (!data) return;
    document.querySelectorAll("#cartCount, #drawerCount").forEach((el) => {
      el.textContent = data.count || 0;
    });
    const wish = document.getElementById("wishCount");
    if (wish) wish.textContent = data.wish_count || 0;
    const total = document.getElementById("drawerTotal");
    if (total) total.textContent = money(data.total);
    const box = document.getElementById("drawerItems");
    if (box) {
      if (!data.items || !data.items.length) {
        box.innerHTML = '<p class="muted text-center" style="padding:24px">Your cart is empty.</p>';
      } else {
        box.innerHTML = data.items
          .map(
            (it) => `<div class="mini-item">
              <img src="${it.image}" alt="">
              <div>
                <a href="/shop/product/${it.id}/${it.slug}">${it.name}</a>
                <div class="qty-step" data-pid="${it.id}">
                  <button type="button" data-act="-">−</button>
                  <input value="${it.qty}" readonly>
                  <button type="button" data-act="+">+</button>
                </div>
                <small>${money(it.line)}</small>
              </div>
              <button class="mini-remove" data-remove="${it.id}">✕</button>
            </div>`
          )
          .join("");
      }
    }
    (data.wishlist_ids || []).forEach((id) => {
      document.querySelectorAll('.like-btn[data-pid="' + id + '"]').forEach((b) => b.classList.add("on"));
    });
    document.querySelectorAll(".like-btn[data-pid]").forEach((b) => {
      const id = Number(b.dataset.pid);
      if (!(data.wishlist_ids || []).includes(id)) b.classList.remove("on");
    });
    document.querySelectorAll("[data-line-total]").forEach((el) => {
      const id = Number(el.dataset.lineTotal);
      const item = (data.items || []).find((x) => x.id === id);
      if (item) el.textContent = money(item.line);
    });
    const pageTotal = document.getElementById("pageCartTotal");
    if (pageTotal) pageTotal.textContent = money(data.total);
    const pageSub = document.getElementById("pageCartSub");
    if (pageSub) pageSub.textContent = money(data.subtotal);
    const pageShip = document.getElementById("pageCartShip");
    if (pageShip) pageShip.textContent = money(data.shipping);
    const pageDisc = document.getElementById("pageCartDisc");
    if (pageDisc) pageDisc.textContent = money(data.discount || 0);
  }

  function openDrawer(id, on) {
    const el = document.getElementById(id);
    const overlay = document.getElementById("overlay");
    if (!el) return;
    el.classList.toggle("open", on);
    const anyOpen = document.querySelector(".drawer.open");
    if (overlay) overlay.classList.toggle("open", !!anyOpen);
  }

  const menuBtn = document.querySelector(".cats-btn");
  const mega = document.querySelector(".mega");
  if (menuBtn && mega) {
    menuBtn.addEventListener("click", function (e) {
      e.preventDefault();
      mega.classList.toggle("open");
    });
    document.addEventListener("click", function (e) {
      if (!mega.contains(e.target) && !menuBtn.contains(e.target)) mega.classList.remove("open");
    });
  }

  const cookieBar = document.getElementById("cookieBar");
  const cookieBtn = document.getElementById("cookieAccept");
  if (cookieBar && cookieBtn) {
    if (localStorage.getItem("1111_cookies") === "1") cookieBar.classList.add("hidden");
    cookieBtn.addEventListener("click", function () {
      localStorage.setItem("1111_cookies", "1");
      cookieBar.classList.add("hidden");
    });
  }

  document.querySelectorAll("[data-slider]").forEach(function (root) {
    const slides = root.querySelectorAll(".swiper-slide");
    if (!slides.length) return;
    let i = 0;
    const bullets = root.querySelector(".swiper-pagination");
    if (bullets) {
      slides.forEach((_, idx) => {
        const b = document.createElement("span");
        b.className = "swiper-pagination-bullet" + (idx === 0 ? " swiper-pagination-bullet-active" : "");
        b.addEventListener("click", () => show(idx));
        bullets.appendChild(b);
      });
    }
    function show(n) {
      i = (n + slides.length) % slides.length;
      slides.forEach((s, idx) => {
        s.style.display = idx === i ? "block" : "none";
      });
      if (bullets) {
        bullets.querySelectorAll(".swiper-pagination-bullet").forEach((b, idx) => {
          b.classList.toggle("swiper-pagination-bullet-active", idx === i);
        });
      }
    }
    show(0);
    const next = root.querySelector(".swiper-button-next");
    const prev = root.querySelector(".swiper-button-prev");
    if (next) next.addEventListener("click", () => show(i + 1));
    if (prev) prev.addEventListener("click", () => show(i - 1));
    if (root.dataset.autoplay) setInterval(() => show(i + 1), 5000);
  });

  const endEl = document.getElementById("flash-end");
  if (endEl) {
    const end = new Date(endEl.dataset.end.replace(/-/g, "/")).getTime();
    function tick() {
      const distance = end - Date.now();
      const h = document.getElementById("flash-hours");
      const m = document.getElementById("flash-minutes");
      const s = document.getElementById("flash-seconds");
      if (!h) return;
      if (isNaN(distance) || distance <= 0) {
        h.textContent = m.textContent = s.textContent = "00";
        return;
      }
      const hours = Math.floor(distance / 3600000);
      const minutes = Math.floor((distance % 3600000) / 60000);
      const seconds = Math.floor((distance % 60000) / 1000);
      h.textContent = String(hours).padStart(2, "0");
      m.textContent = String(minutes).padStart(2, "0");
      s.textContent = String(seconds).padStart(2, "0");
    }
    tick();
    setInterval(tick, 1000);
  }

  document.getElementById("openCart")?.addEventListener("click", () => {
    fetch("/api/cart")
      .then((r) => r.json())
      .then((d) => {
        paintCart(d);
        openDrawer("cartDrawer", true);
      });
  });
  document.getElementById("closeCart")?.addEventListener("click", () => openDrawer("cartDrawer", false));
  document.getElementById("openMenu")?.addEventListener("click", (e) => {
    e.preventDefault();
    openDrawer("menuDrawer", true);
  });
  document.getElementById("closeMenu")?.addEventListener("click", () => openDrawer("menuDrawer", false));
  document.getElementById("overlay")?.addEventListener("click", () => {
    openDrawer("cartDrawer", false);
    openDrawer("menuDrawer", false);
  });

  document.addEventListener("click", function (e) {
    const add = e.target.closest("[data-add]");
    if (add) {
      e.preventDefault();
      const qtyInput = document.querySelector("[name=qty]");
      const qty = qtyInput ? Number(qtyInput.value || 1) : 1;
      post("/api/cart/add", { pid: Number(add.dataset.add), qty }).then((d) => {
        paintCart(d);
        toast(d.message || "Added");
        openDrawer("cartDrawer", true);
      });
    }
    const like = e.target.closest(".like-btn[data-pid]");
    if (like) {
      e.preventDefault();
      post("/api/wishlist/toggle", { pid: Number(like.dataset.pid) }).then((d) => {
        paintCart(d);
        toast(d.message);
      });
    }
    const rem = e.target.closest("[data-remove]");
    if (rem) {
      e.preventDefault();
      post("/api/cart/remove", { pid: Number(rem.dataset.remove) }).then((d) => {
        paintCart(d);
        toast(d.message);
        if (rem.closest("tr")) rem.closest("tr").remove();
      });
    }
    const step = e.target.closest(".qty-step button");
    if (step) {
      const wrap = step.closest(".qty-step");
      const input = wrap.querySelector("input");
      let qty = Number(input.value || 1);
      qty = step.dataset.act === "+" ? qty + 1 : Math.max(0, qty - 1);
      input.value = qty;
      if (wrap.dataset.pid) {
        post("/api/cart/update", { pid: Number(wrap.dataset.pid), qty }).then(paintCart);
      }
    }
  });

  const search = document.getElementById("liveSearch");
  const suggest = document.getElementById("searchSuggest");
  let t;
  if (search && suggest) {
    search.addEventListener("input", function () {
      clearTimeout(t);
      const q = search.value.trim();
      if (q.length < 2) {
        suggest.classList.remove("open");
        return;
      }
      t = setTimeout(() => {
        fetch("/api/search?q=" + encodeURIComponent(q))
          .then((r) => r.json())
          .then((d) => {
            if (!d.results.length) {
              suggest.innerHTML = "<p class='muted' style='padding:10px'>No matches</p>";
            } else {
              suggest.innerHTML = d.results
                .map(
                  (p) =>
                    `<a href="${p.url}"><img src="${p.image}" alt=""><span>${p.name}<br><small>${money(p.price)}</small></span></a>`
                )
                .join("");
            }
            suggest.classList.add("open");
          });
      }, 180);
    });
    document.addEventListener("click", (e) => {
      if (!suggest.contains(e.target) && e.target !== search) suggest.classList.remove("open");
    });
  }

  document.getElementById("deliverSelect")?.addEventListener("change", function () {
    if (!this.value) return;
    post("/api/location", { area: this.value }).then(() => toast("Delivering to " + this.value));
  });
  document.getElementById("langSelect")?.addEventListener("change", function () {
    window.location = "/lang/" + this.value;
  });

  document.getElementById("couponForm")?.addEventListener("submit", function (e) {
    e.preventDefault();
    const code = this.querySelector("[name=code]").value;
    post("/api/coupon", { code }).then((d) => {
      paintCart(d);
      toast(d.message || "Updated");
    }).catch(() => toast("Invalid coupon"));
  });
})();
