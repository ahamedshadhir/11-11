export type Category = {
  id: string;
  name: string;
  nameAr: string;
  image: string;
};

export type Product = {
  id: string;
  name: string;
  slug: string;
  description: string;
  image: string;
  imageHero: string;
  price: number;
  compareAt: number;
  stock: number;
  rating: number;
  categoryId: string;
};

const dj = (path: string, file = "thumbnail.webp") =>
  `https://cdn.dummyjson.com/product-images/${path}/${file}`;

export const CATEGORIES: Category[] = [
  {
    id: "computers",
    name: "Computer & Laptop",
    nameAr: "حاسوب ولابتوب",
    image: dj("laptops/apple-macbook-pro-14-inch-space-grey"),
  },
  {
    id: "phones",
    name: "SmartPhone",
    nameAr: "هواتف",
    image: dj("smartphones/iphone-13-pro"),
  },
  {
    id: "audio",
    name: "Headphones",
    nameAr: "سماعات",
    image: dj("mobile-accessories/apple-airpods-max-silver"),
  },
  {
    id: "accessories",
    name: "Accessories",
    nameAr: "إكسسوارات",
    image: dj("mobile-accessories/apple-iphone-charger"),
  },
  {
    id: "photo",
    name: "Camera & Photo",
    nameAr: "كاميرات",
    image: dj("mobile-accessories/monopod"),
  },
  {
    id: "home",
    name: "TV & Homes",
    nameAr: "المنزل",
    image: dj("mobile-accessories/amazon-echo-plus"),
  },
  {
    id: "fashion",
    name: "Fashion",
    nameAr: "أزياء",
    image: dj("mens-shoes/nike-air-jordan-1-red-and-black"),
  },
];

type Item = {
  name: string;
  path: string;
  categoryId: string;
  price: number;
  description: string;
};

const RAW: Item[] = [
  { name: "iPhone 13 Pro", path: "smartphones/iphone-13-pro", categoryId: "phones", price: 3299, description: "Pro camera system, Super Retina XDR, A15 Bionic." },
  { name: "iPhone X", path: "smartphones/iphone-x", categoryId: "phones", price: 1499, description: "OLED Super Retina, Face ID, wireless charging." },
  { name: "iPhone 6", path: "smartphones/iphone-6", categoryId: "phones", price: 599, description: "Classic 4.7-inch iPhone, still a reliable daily driver." },
  { name: "Samsung Galaxy S10", path: "smartphones/samsung-galaxy-s10", categoryId: "phones", price: 1899, description: "Dynamic AMOLED, triple camera, wireless PowerShare." },
  { name: "Samsung Galaxy S8", path: "smartphones/samsung-galaxy-s8", categoryId: "phones", price: 999, description: "Infinity Display, dual-pixel camera, water resistant." },
  { name: "Samsung Galaxy S7", path: "smartphones/samsung-galaxy-s7", categoryId: "phones", price: 749, description: "Compact flagship with microSD and IP68." },
  { name: "Oppo F19 Pro Plus", path: "smartphones/oppo-f19-pro-plus", categoryId: "phones", price: 899, description: "AMOLED, 48MP quad camera, 33W fast charge." },
  { name: "Oppo A57", path: "smartphones/oppo-a57", categoryId: "phones", price: 499, description: "Big battery, dual camera, ColorOS everyday phone." },
  { name: "Oppo K1", path: "smartphones/oppo-k1", categoryId: "phones", price: 549, description: "In-display fingerprint, 25MP front camera." },
  { name: "Realme XT", path: "smartphones/realme-xt", categoryId: "phones", price: 679, description: "64MP quad camera, Super AMOLED, VOOC charge." },
  { name: "Realme C35", path: "smartphones/realme-c35", categoryId: "phones", price: 399, description: "Clean design, 50MP camera, 5000mAh battery." },
  { name: "Realme X", path: "smartphones/realme-x", categoryId: "phones", price: 629, description: "Pop-up selfie, AMOLED, VOOC flash charge." },
  { name: "Vivo X21", path: "smartphones/vivo-x21", categoryId: "phones", price: 719, description: "In-display fingerprint pioneer, dual camera." },
  { name: "Vivo S1", path: "smartphones/vivo-s1", categoryId: "phones", price: 569, description: "Punch-hole display, 32MP selfie, Funtouch OS." },
  { name: "Vivo V9", path: "smartphones/vivo-v9", categoryId: "phones", price: 529, description: "FullView display, dual rear camera." },
  { name: "MacBook Pro 14", path: "laptops/apple-macbook-pro-14-inch-space-grey", categoryId: "computers", price: 7499, description: "14-inch Liquid Retina XDR, M-series performance." },
  { name: "Dell XPS 13", path: "laptops/new-dell-xps-13-9300-laptop", categoryId: "computers", price: 5299, description: "InfinityEdge ultrabook, all-day battery." },
  { name: "Huawei MateBook X Pro", path: "laptops/huawei-matebook-x-pro", categoryId: "computers", price: 4599, description: "3K touchscreen, hidden camera, thin metal body." },
  { name: "Lenovo Yoga 920", path: "laptops/lenovo-yoga-920", categoryId: "computers", price: 3899, description: "360° 2-in-1, 4K option, all-day hinge." },
  { name: "Asus Zenbook Pro", path: "laptops/asus-zenbook-pro-dual-screen-laptop", categoryId: "computers", price: 6199, description: "Dual-screen creator laptop, StudioBook class." },
  { name: "iPad Mini", path: "tablets/ipad-mini-2021-starlight", categoryId: "computers", price: 2199, description: "A15, USB-C, compact 8.3-inch Liquid Retina." },
  { name: "Galaxy Tab S8+", path: "tablets/samsung-galaxy-tab-s8-plus-grey", categoryId: "computers", price: 2899, description: "Super AMOLED, S Pen, DeX desktop mode." },
  { name: "Galaxy Tab White", path: "tablets/samsung-galaxy-tab-white", categoryId: "computers", price: 1299, description: "Everyday Android tablet, long battery life." },
  { name: "Apple AirPods", path: "mobile-accessories/apple-airpods", categoryId: "audio", price: 699, description: "H2 chip, Adaptive EQ, MagSafe charging case." },
  { name: "AirPods Max Silver", path: "mobile-accessories/apple-airpods-max-silver", categoryId: "audio", price: 2199, description: "Computational audio, ANC, aluminum cups." },
  { name: "Beats Flex Earphones", path: "mobile-accessories/beats-flex-wireless-earphones", categoryId: "audio", price: 249, description: "Magnetic buds, Apple W1, all-day battery." },
  { name: "Apple Watch Series 4", path: "mobile-accessories/apple-watch-series-4-gold", categoryId: "fashion", price: 1299, description: "ECG, fall detection, always-on option." },
  { name: "iPhone Charger", path: "mobile-accessories/apple-iphone-charger", categoryId: "accessories", price: 89, description: "Official USB power adapter for iPhone." },
  { name: "MagSafe Battery Pack", path: "mobile-accessories/apple-magsafe-battery-pack", categoryId: "accessories", price: 399, description: "Snap-on pack, MagSafe aligned charging." },
  { name: "AirPower Charger", path: "mobile-accessories/apple-airpower-wireless-charger", categoryId: "accessories", price: 199, description: "Wireless pad for iPhone and AirPods." },
  { name: "HomePod Mini", path: "mobile-accessories/apple-homepod-mini-cosmic-grey", categoryId: "home", price: 449, description: "360° audio, Siri, smart home hub." },
  { name: "Echo Plus", path: "mobile-accessories/amazon-echo-plus", categoryId: "home", price: 399, description: "Alexa speaker with built-in Zigbee hub." },
  { name: "iPhone 12 Silicone Case", path: "mobile-accessories/iphone-12-silicone-case-with-magsafe-plum", categoryId: "accessories", price: 149, description: "Soft-touch silicone, MagSafe aligned." },
  { name: "Selfie Stick", path: "mobile-accessories/selfie-stick-monopod", categoryId: "photo", price: 79, description: "Extendable monopod for phones." },
  { name: "Monopod", path: "mobile-accessories/monopod", categoryId: "photo", price: 129, description: "Lightweight photo monopod, travel ready." },
  { name: "Rolex Datejust", path: "mens-watches/rolex-datejust", categoryId: "fashion", price: 28999, description: "Oystersteel Datejust, fluted bezel." },
  { name: "Rolex Submariner", path: "mens-watches/rolex-submariner-watch", categoryId: "fashion", price: 34999, description: "Dive watch, Cerachrom bezel, 300m." },
  { name: "Rolex Cellini Date", path: "mens-watches/rolex-cellini-date-black-dial", categoryId: "fashion", price: 25999, description: "18k Cellini, black dial, dress watch." },
  { name: "Longines Master", path: "mens-watches/longines-master-collection", categoryId: "fashion", price: 8999, description: "Automatic chronograph, moonphase option." },
  { name: "Leather Belt Watch", path: "mens-watches/brown-leather-belt-watch", categoryId: "fashion", price: 1299, description: "Classic field watch, leather strap." },
  { name: "Nike Air Jordan 1", path: "mens-shoes/nike-air-jordan-1-red-and-black", categoryId: "fashion", price: 899, description: "Bred colourway, leather upper, Air sole." },
  { name: "Puma Future Rider", path: "mens-shoes/puma-future-rider-trainers", categoryId: "fashion", price: 449, description: "Retro runner, Federbein sole." },
  { name: "Sports Sneakers", path: "mens-shoes/sports-sneakers-off-white-red", categoryId: "fashion", price: 399, description: "Lightweight trainers, everyday wear." },
  { name: "Classic Sunglasses", path: "sunglasses/classic-sun-glasses", categoryId: "fashion", price: 299, description: "UV400 classic frames." },
  { name: "Black Sunglasses", path: "sunglasses/black-sun-glasses", categoryId: "fashion", price: 279, description: "Matte black acetate, full UV." },
  { name: "Prada Bag", path: "womens-bags/prada-women-bag", categoryId: "fashion", price: 4599, description: "Saffiano leather, structured silhouette." },
  { name: "Leather Handbag", path: "womens-bags/heshe-women's-leather-bag", categoryId: "fashion", price: 899, description: "Full-grain leather, detachable strap." },
  { name: "Black Handbag", path: "womens-bags/women-handbag-black", categoryId: "fashion", price: 649, description: "Everyday black tote, zip top." },
  { name: "Blue Handbag", path: "womens-bags/blue-women's-handbag", categoryId: "fashion", price: 679, description: "Structured blue leather bag." },
  { name: "White Backpack", path: "womens-bags/white-faux-leather-backpack", categoryId: "fashion", price: 429, description: "Clean white backpack, laptop sleeve." },
];

export const PRODUCTS: Product[] = RAW.map((item, i) => ({
  id: `p-${String(i + 1).padStart(2, "0")}`,
  name: item.name,
  slug: item.name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, ""),
  description: item.description,
  image: dj(item.path),
  imageHero: dj(item.path),
  price: item.price,
  compareAt: Math.round(item.price * 1.18),
  stock: 24 + (i % 20),
  rating: 4.2 + ((i * 7) % 8) / 10,
  categoryId: item.categoryId,
}));

export const HERO_IMAGE = dj("mobile-accessories/apple-airpods-max-silver");

export const QATAR_AREAS = [
  "Doha",
  "Al Wakrah",
  "Al Rayyan",
  "Lusail",
  "The Pearl",
  "West Bay",
  "Al Khor",
  "Msheireb",
];

export function getProduct(slug: string) {
  return PRODUCTS.find((p) => p.slug === slug || p.id === slug);
}

export function byCategory(id?: string) {
  if (!id) return PRODUCTS;
  return PRODUCTS.filter((p) => p.categoryId === id);
}

export function searchProducts(q: string) {
  const s = q.trim().toLowerCase();
  if (!s) return PRODUCTS;
  return PRODUCTS.filter(
    (p) => p.name.toLowerCase().includes(s) || p.description.toLowerCase().includes(s),
  );
}
