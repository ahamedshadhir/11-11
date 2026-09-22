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

const dj = (path: string, file = "thumbnail.webp") => {
  const segs = path
    .split("/")
    .map((part) => encodeURIComponent(part))
    .join("/");
  return `https://cdn.dummyjson.com/product-images/${segs}/${file}`;
};

export const CATEGORIES: Category[] = [
  {
    id: "computers",
    name: "Computers",
    nameAr: "حواسيب",
    image: dj("laptops/apple-macbook-pro-14-inch-space-grey"),
  },
  {
    id: "phones",
    name: "Smartphones",
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
    id: "home",
    name: "Home & Kitchen",
    nameAr: "المنزل والمطبخ",
    image: dj("furniture/annibale-colombo-sofa"),
  },
  {
    id: "fashion",
    name: "Fashion",
    nameAr: "أزياء",
    image: dj("mens-shoes/nike-air-jordan-1-red-and-black"),
  },
  {
    id: "beauty",
    name: "Beauty",
    nameAr: "جمال",
    image: dj("beauty/red-lipstick"),
  },
  {
    id: "sports",
    name: "Sports",
    nameAr: "رياضة",
    image: dj("sports-accessories/football"),
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
  { name: "AirPods Max Silver", path: "mobile-accessories/apple-airpods-max-silver", categoryId: "audio", price: 2199, description: "Computational audio, active noise cancelling, aluminum cups." },
  { name: "MacBook Pro 14", path: "laptops/apple-macbook-pro-14-inch-space-grey", categoryId: "computers", price: 7499, description: "14-inch Liquid Retina XDR, M-series performance." },
  { name: "iPhone 13 Pro", path: "smartphones/iphone-13-pro", categoryId: "phones", price: 3299, description: "Pro camera system, Super Retina XDR, A15 Bionic." },
  { name: "Nike Air Jordan 1", path: "mens-shoes/nike-air-jordan-1-red-and-black", categoryId: "fashion", price: 899, description: "Bred colourway, leather upper, Air sole." },
  { name: "Chanel Coco Noir Eau De", path: "fragrances/chanel-coco-noir-eau-de", categoryId: "beauty", price: 749, description: "Oriental floral eau de parfum, full-size bottle." },
  { name: "Annibale Colombo Sofa", path: "furniture/annibale-colombo-sofa", categoryId: "home", price: 8999, description: "Italian leather sofa, deep seat, kiln-dried frame." },
  { name: "Football", path: "sports-accessories/football", categoryId: "sports", price: 129, description: "Match football, machine-stitched, training and play." },
  { name: "Boxed Blender", path: "kitchen-accessories/boxed-blender", categoryId: "home", price: 349, description: "Countertop blender with jug, everyday kitchen duty." },
  { name: "Samsung Galaxy S10", path: "smartphones/samsung-galaxy-s10", categoryId: "phones", price: 1899, description: "Dynamic AMOLED, triple camera, wireless PowerShare." },
  { name: "Oppo F19 Pro Plus", path: "smartphones/oppo-f19-pro-plus", categoryId: "phones", price: 899, description: "AMOLED, 48MP quad camera, 33W fast charge." },
  { name: "Realme C35", path: "smartphones/realme-c35", categoryId: "phones", price: 399, description: "Clean design, 50MP camera, 5000mAh battery." },
  { name: "Dell XPS 13", path: "laptops/new-dell-xps-13-9300-laptop", categoryId: "computers", price: 5299, description: "InfinityEdge ultrabook, all-day battery." },
  { name: "Huawei MateBook X Pro", path: "laptops/huawei-matebook-x-pro", categoryId: "computers", price: 4599, description: "3K touchscreen, hidden camera, thin metal body." },
  { name: "Lenovo Yoga 920", path: "laptops/lenovo-yoga-920", categoryId: "computers", price: 3899, description: "360° 2-in-1, 4K option, all-day hinge." },
  { name: "Asus Zenbook Pro", path: "laptops/asus-zenbook-pro-dual-screen-laptop", categoryId: "computers", price: 6199, description: "Dual-screen creator laptop, StudioBook class." },
  { name: "iPad Mini", path: "tablets/ipad-mini-2021-starlight", categoryId: "computers", price: 2199, description: "A15, USB-C, compact 8.3-inch Liquid Retina." },
  { name: "Galaxy Tab S8+", path: "tablets/samsung-galaxy-tab-s8-plus-grey", categoryId: "computers", price: 2899, description: "Super AMOLED, S Pen, DeX desktop mode." },
  { name: "Galaxy Tab White", path: "tablets/samsung-galaxy-tab-white", categoryId: "computers", price: 1299, description: "Everyday Android tablet, long battery life." },
  { name: "Apple AirPods", path: "mobile-accessories/apple-airpods", categoryId: "audio", price: 699, description: "H2 chip, Adaptive EQ, MagSafe charging case." },
  { name: "Beats Flex Earphones", path: "mobile-accessories/beats-flex-wireless-earphones", categoryId: "audio", price: 249, description: "Magnetic buds, Apple W1, all-day battery." },
  { name: "iPhone Charger", path: "mobile-accessories/apple-iphone-charger", categoryId: "accessories", price: 89, description: "Official USB power adapter for iPhone." },
  { name: "MagSafe Battery Pack", path: "mobile-accessories/apple-magsafe-battery-pack", categoryId: "accessories", price: 399, description: "Snap-on pack, MagSafe aligned charging." },
  { name: "AirPower Charger", path: "mobile-accessories/apple-airpower-wireless-charger", categoryId: "accessories", price: 199, description: "Wireless pad for iPhone and AirPods." },
  { name: "iPhone 12 Silicone Case", path: "mobile-accessories/iphone-12-silicone-case-with-magsafe-plum", categoryId: "accessories", price: 149, description: "Soft-touch silicone, MagSafe aligned." },
  { name: "Selfie Stick", path: "mobile-accessories/selfie-stick-monopod", categoryId: "accessories", price: 79, description: "Extendable monopod for phones." },
  { name: "Monopod", path: "mobile-accessories/monopod", categoryId: "accessories", price: 129, description: "Lightweight photo monopod, travel ready." },
  { name: "Selfie Lamp", path: "mobile-accessories/selfie-lamp-with-iphone", categoryId: "accessories", price: 99, description: "Ring light clip for phone selfies and calls." },
  { name: "HomePod Mini", path: "mobile-accessories/apple-homepod-mini-cosmic-grey", categoryId: "home", price: 449, description: "360° audio, Siri, smart home hub." },
  { name: "Echo Plus", path: "mobile-accessories/amazon-echo-plus", categoryId: "home", price: 399, description: "Alexa speaker with built-in Zigbee hub." },
  { name: "Bedside Table African Cherry", path: "furniture/bedside-table-african-cherry", categoryId: "home", price: 1299, description: "Solid cherry nightstand, drawer storage." },
  { name: "Knoll Saarinen Chair", path: "furniture/knoll-saarinen-executive-conference-chair", categoryId: "home", price: 4599, description: "Executive conference chair, leather, swivel." },
  { name: "Annibale Colombo Bed", path: "furniture/annibale-colombo-bed", categoryId: "home", price: 12999, description: "Upholstered Italian bed, king-size frame." },
  { name: "Table Lamp", path: "home-decoration/table-lamp", categoryId: "home", price: 229, description: "Bedside lamp, warm shade, compact base." },
  { name: "Plant Pot", path: "home-decoration/plant-pot", categoryId: "home", price: 89, description: "Ceramic planter for indoor plants." },
  { name: "Family Tree Photo Frame", path: "home-decoration/family-tree-photo-frame", categoryId: "home", price: 159, description: "Multi-opening frame for family prints." },
  { name: "House Showpiece Plant", path: "home-decoration/house-showpiece-plant", categoryId: "home", price: 119, description: "Faux indoor plant, no watering required." },
  { name: "Microwave Oven", path: "kitchen-accessories/microwave-oven", categoryId: "home", price: 499, description: "Countertop microwave for everyday reheating." },
  { name: "Carbon Steel Wok", path: "kitchen-accessories/carbon-steel-wok", categoryId: "home", price: 189, description: "Round-bottom wok, high-heat stir fry." },
  { name: "Chopping Board", path: "kitchen-accessories/chopping-board", categoryId: "home", price: 69, description: "Wooden cutting board, juice groove." },
  { name: "Electric Stove", path: "kitchen-accessories/electric-stove", categoryId: "home", price: 279, description: "Portable electric hot plate, two zones." },
  { name: "Silver Pot With Glass Cap", path: "kitchen-accessories/silver-pot-with-glass-cap", categoryId: "home", price: 149, description: "Stainless casserole with glass lid." },
  { name: "Mug Tree Stand", path: "kitchen-accessories/mug-tree-stand", categoryId: "home", price: 59, description: "Counter mug tree, six hooks." },
  { name: "Spice Rack", path: "kitchen-accessories/spice-rack", categoryId: "home", price: 89, description: "Tiered rack for jars, kitchen counter." },
  { name: "Pan", path: "kitchen-accessories/pan", categoryId: "home", price: 129, description: "Non-stick frying pan, everyday cooking." },
  { name: "Apple Watch Series 4", path: "mobile-accessories/apple-watch-series-4-gold", categoryId: "fashion", price: 1299, description: "ECG, fall detection, gold aluminum case." },
  { name: "Rolex Datejust", path: "mens-watches/rolex-datejust", categoryId: "fashion", price: 28999, description: "Oystersteel Datejust, fluted bezel." },
  { name: "Rolex Submariner", path: "mens-watches/rolex-submariner-watch", categoryId: "fashion", price: 34999, description: "Dive watch, Cerachrom bezel, 300m." },
  { name: "Longines Master", path: "mens-watches/longines-master-collection", categoryId: "fashion", price: 8999, description: "Automatic chronograph, moonphase option." },
  { name: "Leather Belt Watch", path: "mens-watches/brown-leather-belt-watch", categoryId: "fashion", price: 1299, description: "Classic field watch, leather strap." },
  { name: "IWC Ingenieur Automatic", path: "womens-watches/iwc-ingenieur-automatic-steel", categoryId: "fashion", price: 18999, description: "Steel Ingenieur, automatic, integrated bracelet." },
  { name: "Rolex Datejust Women", path: "womens-watches/rolex-datejust-women", categoryId: "fashion", price: 26999, description: "Ladies Datejust, oyster bracelet." },
  { name: "Watch Gold for Women", path: "womens-watches/watch-gold-for-women", categoryId: "fashion", price: 1599, description: "Gold-tone dress watch, slim case." },
  { name: "Puma Future Rider", path: "mens-shoes/puma-future-rider-trainers", categoryId: "fashion", price: 449, description: "Retro runner, Federbein sole." },
  { name: "Sports Sneakers", path: "mens-shoes/sports-sneakers-off-white-red", categoryId: "fashion", price: 399, description: "Lightweight trainers, everyday wear." },
  { name: "Nike Baseball Cleats", path: "mens-shoes/nike-baseball-cleats", categoryId: "fashion", price: 529, description: "Molded cleats, locked-in baseball fit." },
  { name: "Classic Sunglasses", path: "sunglasses/classic-sun-glasses", categoryId: "fashion", price: 299, description: "UV400 classic frames." },
  { name: "Black Sunglasses", path: "sunglasses/black-sun-glasses", categoryId: "fashion", price: 279, description: "Matte black acetate, full UV." },
  { name: "Green and Black Glasses", path: "sunglasses/green-and-black-glasses", categoryId: "fashion", price: 259, description: "Two-tone frames, everyday sun." },
  { name: "Prada Bag", path: "womens-bags/prada-women-bag", categoryId: "fashion", price: 4599, description: "Saffiano leather, structured silhouette." },
  { name: "Leather Handbag", path: "womens-bags/heshe-women's-leather-bag", categoryId: "fashion", price: 899, description: "Full-grain leather, detachable strap." },
  { name: "Black Handbag", path: "womens-bags/women-handbag-black", categoryId: "fashion", price: 649, description: "Everyday black tote, zip top." },
  { name: "Blue Handbag", path: "womens-bags/blue-women's-handbag", categoryId: "fashion", price: 679, description: "Structured blue leather bag." },
  { name: "White Backpack", path: "womens-bags/white-faux-leather-backpack", categoryId: "fashion", price: 429, description: "Clean white backpack, laptop sleeve." },
  { name: "Blue and Black Check Shirt", path: "mens-shirts/blue-&-black-check-shirt", categoryId: "fashion", price: 199, description: "Cotton check shirt, button-down collar." },
  { name: "Man Plaid Shirt", path: "mens-shirts/man-plaid-shirt", categoryId: "fashion", price: 179, description: "Soft plaid, regular fit, chest pocket." },
  { name: "Calvin Klein Heel Shoes", path: "womens-shoes/calvin-klein-heel-shoes", categoryId: "fashion", price: 799, description: "Pointed heel, leather upper." },
  { name: "Black Women's Gown", path: "womens-dresses/black-women's-gown", categoryId: "fashion", price: 1299, description: "Floor-length black gown, evening cut." },
  { name: "Green Crystal Earring", path: "womens-jewellery/green-crystal-earring", categoryId: "fashion", price: 349, description: "Crystal drop earrings, green stone." },
  { name: "Essence Mascara Lash Princess", path: "beauty/essence-mascara-lash-princess", categoryId: "beauty", price: 39, description: "Volume mascara, defined lashes." },
  { name: "Eyeshadow Palette with Mirror", path: "beauty/eyeshadow-palette-with-mirror", categoryId: "beauty", price: 89, description: "Multi-shade palette, built-in mirror." },
  { name: "Red Lipstick", path: "beauty/red-lipstick", categoryId: "beauty", price: 59, description: "Classic red lipstick, creamy finish." },
  { name: "Red Nail Polish", path: "beauty/red-nail-polish", categoryId: "beauty", price: 29, description: "High-shine red lacquer." },
  { name: "Calvin Klein CK One", path: "fragrances/calvin-klein-ck-one", categoryId: "beauty", price: 299, description: "Unisex citrus eau de toilette." },
  { name: "Dior J'adore", path: "fragrances/dior-j'adore", categoryId: "beauty", price: 799, description: "Floral feminine eau de parfum." },
  { name: "Gucci Bloom Eau de", path: "fragrances/gucci-bloom-eau-de", categoryId: "beauty", price: 689, description: "White floral, tuberose and jasmine." },
  { name: "Dolce Shine Eau de", path: "fragrances/dolce-shine-eau-de", categoryId: "beauty", price: 559, description: "Fruity floral, sunny bottle." },
  { name: "Olay Body Wash", path: "skin-care/olay-ultra-moisture-shea-butter-body-wash", categoryId: "beauty", price: 49, description: "Shea butter moisture wash." },
  { name: "Vaseline Men Lotion", path: "skin-care/vaseline-men-body-and-face-lotion", categoryId: "beauty", price: 39, description: "Body and face lotion for men." },
  { name: "Attitude Hand Soap", path: "skin-care/attitude-super-leaves-hand-soap", categoryId: "beauty", price: 35, description: "Plant-based hand soap, super leaves." },
  { name: "Basketball", path: "sports-accessories/basketball", categoryId: "sports", price: 119, description: "Indoor/outdoor basketball, standard size." },
  { name: "Cricket Bat", path: "sports-accessories/cricket-bat", categoryId: "sports", price: 349, description: "Willow cricket bat, mid-blade pickup." },
  { name: "Tennis Racket", path: "sports-accessories/tennis-racket", categoryId: "sports", price: 399, description: "Graphite frame, strung, adult grip." },
  { name: "Volleyball", path: "sports-accessories/volleyball", categoryId: "sports", price: 99, description: "Official-size volleyball, indoor play." },
  { name: "Cricket Helmet", path: "sports-accessories/cricket-helmet", categoryId: "sports", price: 279, description: "Grille helmet, adjustable fit." },
  { name: "Baseball Glove", path: "sports-accessories/baseball-glove", categoryId: "sports", price: 189, description: "Leather fielding glove, broken-in pocket." },
  { name: "Tennis Ball", path: "sports-accessories/tennis-ball", categoryId: "sports", price: 29, description: "Pressurised tennis ball, training pack." },
  { name: "Cricket Ball", path: "sports-accessories/cricket-ball", categoryId: "sports", price: 49, description: "Leather cricket ball, four-piece." },
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
