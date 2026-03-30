/**
 * @typedef {{ id: string, label: string, href: string }} NavLink
 * @typedef {{ id: string, eyebrow: string, title: string, copy: string, highlight: string, image: string, metrics: string[] }} HeroSlide
 * @typedef {{ id: string, title: string, description: string, icon: string }} TrustPoint
 * @typedef {{ id: string, name: string, subtitle: string, details: string[], buyerFit: string, image: string }} CoffeeSpec
 * @typedef {{ id: string, step: string, title: string, copy: string }} WorkflowStep
 * @typedef {{ id: string, title: string, copy: string, icon: string }} PartnerBenefit
 * @typedef {{ id: string, value: string, label: string, copy: string }} ImpactStat
 * @typedef {{ src: string, alt: string, title: string, description: string }} GalleryItem
 * @typedef {{ fullName: string, companyName: string, businessType: string, email: string, phone: string, monthlyVolume: string, message: string }} WholesaleInquiry
 */

export const navLinks = [
  { id: 'home', label: 'Home', href: '/' },
  { id: 'products', label: 'Products', href: '/#coffee-specs' },
  { id: 'workflow', label: 'How It Works', href: '/#sourcing' },
  { id: 'about', label: 'About Us', href: '/#market-position' },
  { id: 'gallery', label: 'Gallery', href: '/gallery' },
  { id: 'blog', label: 'Blog', href: '/blog' },
  { id: 'partner', label: 'Partner With Us', href: '/#distribution' },
  { id: 'contact', label: 'Contacts', href: '/#inquiry' },
]

/** @type {HeroSlide[]} */
export const heroSlides = [
  {
    id: 'supply',
    eyebrow: 'Welcome to Savana Sips',
    title: 'Best Wholesale Coffee Supply',
    copy:
      'Premium specialty coffee sourced for wholesale partners.',
    highlight: 'Designed for wholesale growth, perfectly aligned with market expectations.',
    image:
      'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1800&q=80',
    metrics: ['Specialty-grade lots', 'Buyer-ready sourcing conversations', 'Wholesale pricing inquiries'],
  },
  {
    id: 'quality',
    eyebrow: 'Premium Grade Selection',
    title: 'Arabica Special Grade Selection',
    copy:
      'High-altitude Arabica with exceptional cup character.',
    highlight: 'Origin-led, perfectly aligned with domestic market expectations.',
    image:
      'https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=1800&q=80',
    metrics: ['High-altitude sourcing', 'Traceable lot narratives', 'Commercially relevant quality'],
  },
  {
    id: 'partnership',
    eyebrow: 'Streamlined Supply Chain',
    title: 'Fast Delivery, Every Time',
    copy:
      'Reliable shipments from origin to your door.',
    highlight: 'Built to help wholesale partners sell with confidence.',
    image:
      'https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=1800&q=80',
    metrics: ['Specification-forward sales', 'Flexible inquiry path', 'Partnership-oriented communication'],
  },
]

/** @type {TrustPoint[]} */
export const trustPoints = [
  {
    id: 'grade',
    title: 'Specialty Grade',
    description: 'AA and high-altitude Arabica for premium wholesale programs.',
    icon: 'badge',
    bgImage: 'https://images.unsplash.com/photo-1497935586351-b67a49e012bf?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 'workflow',
    title: 'Export Ready',
    description: 'Streamlined sourcing and lot-prep for wholesale buyers.',
    icon: 'container',
    bgImage: 'https://images.unsplash.com/photo-1559525839-b184a4d698c7?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 'response',
    title: 'Fast Response',
    description: 'Pricing and samples within one business cycle.',
    icon: 'timer',
    bgImage: 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=600&q=80',
  },
]

/** @type {CoffeeSpec[]} */
export const coffeeSpecs = [
  {
    id: 'aa-grade',
    name: 'AA Grade',
    subtitle: 'Large-bean, bold acidity, clean finish',
    price: 'Premium',
    image: 'https://images.unsplash.com/photo-1559525839-b184a4d698c7?auto=format&fit=crop&w=150&q=80',
  },
  {
    id: 'ab-grade',
    name: 'AB Grade',
    subtitle: 'Versatile mid-grade, balanced cup',
    price: 'Core',
    image: 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=150&q=80',
  },
  {
    id: 'peaberry',
    name: 'Peaberry (PB)',
    subtitle: 'Concentrated flavor, rounded body',
    price: 'Specialty',
    image: 'https://images.unsplash.com/photo-1611162458324-aae1eb4129a4?auto=format&fit=crop&w=150&q=80',
  },
  {
    id: 'estate',
    name: 'Estate Lots',
    subtitle: 'Single-origin, fully traceable',
    price: 'Limited',
    image: 'https://images.unsplash.com/photo-1497935586351-b67a49e012bf?auto=format&fit=crop&w=150&q=80',
  },
  {
    id: 'washed',
    name: 'Washed Process',
    subtitle: 'Bright, clean, classic Kenyan profile',
    price: 'Available',
    image: 'https://images.unsplash.com/photo-1498804103079-a6351b050096?auto=format&fit=crop&w=150&q=80',
  },
  {
    id: 'natural',
    name: 'Natural Process',
    subtitle: 'Fruity, full-bodied, complex sweetness',
    price: 'Seasonal',
    image: 'https://images.unsplash.com/photo-1587734195503-904fca47e0e9?auto=format&fit=crop&w=150&q=80',
  }
]

/** @type {WorkflowStep[]} */
export const workflowSteps = [
  {
    id: 'selection',
    icon: 'MapPin',
    title: 'Source Selection',
    copy: 'High-potential lots and quality-forward farm relationships starting with cup value.',
  },
  {
    id: 'harvest',
    icon: 'Leaf',
    title: 'Harvest & Sorting',
    copy: 'Only the right cherries move forward to protect later chain quality expectations.',
  },
  {
    id: 'processing',
    icon: 'Sun',
    title: 'Processing & Drying',
    copy: 'Washing, fermentation, and raised-bed drying framed as strict quality controls.',
  },
  {
    id: 'export',
    icon: 'Truck',
    title: 'Export Coordination',
    copy: 'Documentation and shipment readiness for importers and distributors.',
  },
]

/** @type {PartnerBenefit[]} */
export const partnerBenefits = [
  {
    id: 'sales',
    title: 'A Story That Sells',
    copy: 'Every lot comes with a real origin story your team can use to win buyers.',
    icon: 'line',
  },
  {
    id: 'buyers',
    title: 'Clear Communication',
    copy: 'Straightforward pricing, specs, and timelines — no guesswork.',
    icon: 'briefcase',
  },
  {
    id: 'quality',
    title: 'Proven Quality',
    copy: 'Specialty-grade coffee with full traceability and transparent grading.',
    icon: 'shield',
  },
  {
    id: 'growth',
    title: 'Built to Grow With You',
    copy: 'Flexible volumes and dedicated support as your business scales.',
    icon: 'ship',
  },
]

/** @type {ImpactStat[]} */
export const impactStats = [
  {
    id: 'elevation',
    value: '1,600-2,100m',
    label: 'Typical high-altitude sourcing range',
    copy: 'Altitude becomes a proof point for cup quality and premium positioning rather than a generic origin claim.',
  },
  {
    id: 'response',
    value: '24-48 hrs',
    label: 'Target wholesale follow-up window',
    copy: 'The inquiry flow is built for pricing, lot availability, and sample conversations that move quickly.',
  },
  {
    id: 'workflow',
    value: '6-Step',
    label: 'Supply-to-distribution workflow',
    copy: 'A concise process narrative helps buyers understand how quality is protected before coffee reaches your warehouse.',
  },
]

export const galleryCategories = ['ALL', 'FARMING', 'PROCESSING', 'ROASTING', 'EXPORT']

/** @type {GalleryItem[]} */
export const galleryItems = [
  {
    src: 'https://images.unsplash.com/photo-1762277142890-24902d58e8f0?auto=format&fit=crop&w=1600&q=80',
    alt: 'Hands holding freshly harvested coffee cherries',
    title: 'Harvest',
    description: 'Operational imagery that supports sourcing credibility and quality handling.',
    category: 'FARMING',
  },
  {
    src: 'https://images.unsplash.com/photo-1761318543563-f5c211a99195?auto=format&fit=crop&w=1600&q=80',
    alt: 'Coffee beans drying outdoors during processing',
    title: 'Drying',
    description: 'The page should show process, not packaging theater.',
    category: 'PROCESSING',
  },
  {
    src: 'https://images.unsplash.com/photo-1640770668482-8e3827119472?auto=format&fit=crop&w=1600&q=80',
    alt: 'Roasting drum filled with coffee beans',
    title: 'Roasting',
    description: 'A closer operational view of premium coffee handling after processing.',
    category: 'ROASTING',
  },
  {
    src: 'https://images.unsplash.com/photo-1703646617698-d61b240cd2f8?auto=format&fit=crop&w=1600&q=80',
    alt: 'Green coffee beans prepared for wholesale review',
    title: 'Green Coffee',
    description: 'Visual detail that supports lot conversations, profiling, and buyer review.',
    category: 'PROCESSING',
  },
  {
    src: 'https://images.unsplash.com/photo-1569718974246-7b898eae87d3?auto=format&fit=crop&w=1600&q=80',
    alt: 'Coffee sacks staged in a warehouse for distribution',
    title: 'Distribution Readiness',
    description: 'Operational visuals reinforce the distributor-first positioning.',
    category: 'EXPORT',
  },
  {
    src: 'https://images.unsplash.com/photo-1650908007715-13db33e2de6c?auto=format&fit=crop&w=1600&q=80',
    alt: 'Coffee farm landscape with cultivated rows',
    title: 'Origin Depth',
    description: 'Kenyan highland origin appears as a subtle but credible quality layer.',
    category: 'FARMING',
  },
]

/** @type {WholesaleInquiry} */
export const initialInquiry = {
  fullName: '',
  companyName: '',
  businessType: 'Importer / Distributor',
  email: '',
  phone: '',
  monthlyVolume: '',
  message: '',
}

export const businessTypes = [
  'Importer / Distributor',
  'Specialty Roaster',
  'Hospitality Supply Group',
  'Multi-Location Cafe Group',
  'Private Label Buyer',
]

export const volumeOptions = [
  'Under 10 bags per month',
  '10-25 bags per month',
  '25-50 bags per month',
  '50+ bags per month',
]

export const companyStats = [
  { id: 1, icon: 'badge', value: '50+', label: 'Wholesale Partners', copy: 'Across North America and Europe' },
  { id: 2, icon: 'MapPin', value: '12+', label: 'Partner Estates', copy: 'High-altitude Kenyan cooperatives' },
  { id: 3, icon: 'container', value: '1.2M+', label: 'Lbs Exported', copy: 'Consistent annual volume' },
  { id: 4, icon: 'shield', value: '88+', label: 'Average Q-score', copy: 'Strictly specialty-grade lots' },
]

export const testimonials = [
  {
    id: 1,
    name: 'David R. Portland',
    role: 'Head Roaster',
    stars: 5,
    copy: 'The quality consistency has allowed us to scale our single-origin program with absolute confidence. They handle the hard work at origin seamlessly.',
    avatar: 'https://images.unsplash.com/photo-1599566150163-29194dcaad36?auto=format&fit=crop&w=150&q=80',
  },
  {
    id: 2,
    name: 'Emily T. Austin',
    role: 'Sourcing Director',
    stars: 5,
    copy: 'Savana Sips intrinsically understands the wholesale timeline. Communication is fast and the green coffee speaks for itself on the cupping table.',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80',
  },
  {
    id: 3,
    name: 'Marcus W. Seattle',
    role: 'Operations Lead',
    stars: 5,
    copy: 'Finding Kenyan lots that hold their brightness out of season is remarkably tough. Their strict drying protocols make a huge difference in shelf life.',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80',
  },
  {
    id: 4,
    name: 'Sarah K. London',
    role: 'Cafe Chain Owner',
    stars: 5,
    copy: 'Transparent pricing and bulletproof logistics. We’ve confidently shifted 30% of our core seasonal menu strictly to their AB grades.',
    avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=150&q=80',
  },
]

export const blogPosts = [
  {
    id: 'coffee-makes-you-poop-during-the-day',
    title: 'Coffee makes you poop during the day because it affects your digestive',
    date: '25 Sep 2021',
    image: 'https://images.unsplash.com/photo-1611162458324-aae1eb4129a4?auto=format&fit=crop&w=800&q=80',
    content: `
      <p>When you drink a cup of coffee, your stomach's production of gastric acid increases. This jump in acid starts the digestive process much faster than a standard drink, triggering early morning bowel movements. Beyond just acid, the caffeine compound itself stimulates the colonic muscles.</p>
      
      <blockquote>
        <p>Photography is the story I fail to put into words get ligula vel, commodo luctus felis. Ut dignissim sapien sit amet molestie rutr</p>
        <cite>Destin Sparks</cite>
      </blockquote>
      
      <p>Research has shown that coffee can induce a 'gastrocolic reflex', which essentially signals your colon to make room for newly digested food. However, contrary to common belief, this response isn't exclusively tied to caffeine—even decaf can prompt a similar (though less pronounced) digestive kick.</p>
      
      <ul>
        <li>Donec arcu lacus, ornare eget ligula vel, commodo luctus felis.</li>
        <li>Ut dignissim sapien sit amet molestie rutrum.</li>
        <li>Orci varius natoque penatibus et magnis dis parturient montes.</li>
        <li>Ut at nulla ut libero mollis viverra sed vitae purus.</li>
      </ul>
      
      <p>Nam dui mauris, congue vel nisi in, tempus gravida enim. Nulla et tristique orci. Pellentesque lectus sapien, maximus id gravida sit amet, tristique non eros. Etiam aliquet, sem vitae sagittis convallis, ante sapien tincidunt nisl, eget dapibus tortor velit quis ex.</p>
    `
  },
  {
    id: 'coffee-with-added-milk-provides-macro-nutrients',
    title: 'Coffee with added milk provides all the macro nutrients in good amounts',
    date: '25 Sep 2021',
    image: 'https://images.unsplash.com/photo-1559525839-b184a4d698c7?auto=format&fit=crop&w=800&q=80',
    content: `
      <p>When milk is added to black coffee, it dramatically shifts the nutritional profile of the beverage. A single splash introduces high-quality proteins, essential fats, and natural carbohydrates. Unlike plain black coffee which holds almost zero calories, a milk-based drink essentially turns into a very light meal replacement.</p>
      
      <blockquote>
        <p>A good cup of coffee is a delicate balance of profound flavors and a comforting routine.</p>
        <cite>Coffee Connoisseur</cite>
      </blockquote>
      
      <p>From a metabolic perspective, the fats present in whole milk slow down caffeine absorption. This minimizes the sudden caffeine 'spike and crash', replacing it with a more sustained, longer-lasting energy release.</p>
      
      <ul>
        <li>Reduces sudden jittery spikes caused by rapid caffeine absorption.</li>
        <li>Adds a healthy source of calcium and fat-soluble vitamins.</li>
        <li>Enhances the overall mouthfeel and textural experience.</li>
      </ul>
    `
  },
  {
    id: 'for-most-people-moderate-coffee-consumption',
    title: 'For most people, moderate coffee consumption can be incorporated',
    date: '25 Sep 2021',
    image: 'https://images.unsplash.com/photo-1497935586351-b67a49e012bf?auto=format&fit=crop&w=800&q=80',
    content: `
      <p>Moderate coffee intake, generally considered around 3 to 4 cups daily, has been heavily researched by health authorities worldwide. Current consensus finds that in a healthy adult diet, this level is entirely safe, provided no pre-existing sensitivities are present.</p>
      
      <ul>
        <li>Maintains a steady release of cognitive-enhancing antioxidants.</li>
        <li>Promotes an active lifestyle and improved mental clarity.</li>
        <li>Safe for consumption within the 3-4 cup threshold.</li>
      </ul>

      <p>Beyond just being safe, long-term observational studies highlight considerable protective health benefits including reduced risks of certain neurological and metabolic conditions. The key distinction researchers make is how the coffee is prepared: high-sugar, heavily processed syrups actively erode these benefits, while consuming it black or with light milk modifications preserves its robust antioxidant profile.</p>
    `
  }
]

