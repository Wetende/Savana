/**
 * @typedef {{ id: string, label: string, href: string }} NavLink
 * @typedef {{ id: string, eyebrow: string, title: string, copy: string, highlight: string, image: string, metrics: string[] }} HeroSlide
 * @typedef {{ id: string, title: string, description: string, icon: string }} TrustPoint
 * @typedef {{ id: string, name: string, subtitle: string, details: string[], buyerFit: string }} CoffeeSpec
 * @typedef {{ id: string, step: string, title: string, copy: string }} WorkflowStep
 * @typedef {{ id: string, title: string, copy: string, icon: string }} PartnerBenefit
 * @typedef {{ id: string, value: string, label: string, copy: string }} ImpactStat
 * @typedef {{ src: string, alt: string, title: string, description: string }} GalleryItem
 * @typedef {{ fullName: string, companyName: string, businessType: string, email: string, phone: string, monthlyVolume: string, message: string }} WholesaleInquiry
 */

/** @type {NavLink[]} */
export const navLinks = [
  { id: 'overview', label: 'Overview', href: '#overview' },
  { id: 'coffee-specs', label: 'Coffee Specs', href: '#coffee-specs' },
  { id: 'sourcing', label: 'Sourcing', href: '#sourcing' },
  { id: 'distribution', label: 'Distribution', href: '#distribution' },
  { id: 'impact', label: 'Impact', href: '#impact' },
  { id: 'contact', label: 'Contact', href: '#inquiry' },
]

/** @type {HeroSlide[]} */
export const heroSlides = [
  {
    id: 'supply',
    eyebrow: 'Wholesale Specialty Coffee for the U.S. Market',
    title: 'Premium Coffee Supply Built for U.S. Distribution',
    copy:
      'Savana Sips helps distributors, import partners, and specialty buyers source premium coffee with clearer communication, stronger origin credibility, and export-ready coordination.',
    highlight: 'Designed for wholesale growth, not direct-to-consumer retail.',
    image:
      'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1800&q=80',
    metrics: ['Specialty-grade lots', 'Buyer-ready sourcing conversations', 'Wholesale pricing inquiries'],
  },
  {
    id: 'quality',
    eyebrow: 'Quality-Led Positioning',
    title: 'Distinctive Cup Quality with Commercial Reliability',
    copy:
      'From high-altitude Arabica profiles to carefully graded AA selections, the offer centers on cup character, traceability, and consistency that fits premium wholesale programs.',
    highlight: 'Origin-led, but always framed through the needs of U.S. buyers.',
    image:
      'https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=1800&q=80',
    metrics: ['High-altitude sourcing', 'Traceable lot narratives', 'Commercially relevant quality'],
  },
  {
    id: 'partnership',
    eyebrow: 'Distribution-Focused Messaging',
    title: 'A Supplier Story Your Sales Team Can Actually Use',
    copy:
      'The brand story stays refined and credible: enough origin depth to support premium positioning, without overwhelming distributor conversations with retail lifestyle messaging.',
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
    title: 'Specialty-Grade Focus',
    description: 'AA and high-altitude Arabica profiles positioned for premium distributor catalogs and specialty programs.',
    icon: 'badge',
  },
  {
    id: 'workflow',
    title: 'Export-Ready Coordination',
    description: 'Clear sourcing, processing, and lot-prep communication designed to reduce friction for wholesale buyers.',
    icon: 'container',
  },
  {
    id: 'story',
    title: 'Origin with Restraint',
    description: 'Kenyan provenance supports the story, but the sales message stays centered on quality, consistency, and buyer confidence.',
    icon: 'leaf',
  },
  {
    id: 'response',
    title: 'Fast Buyer Response',
    description: 'A wholesale-first inquiry flow aimed at pricing, sample requests, and availability conversations within one business cycle.',
    icon: 'timer',
  },
]

/** @type {CoffeeSpec[]} */
export const coffeeSpecs = [
  {
    id: 'aa',
    name: 'AA Selections',
    subtitle: 'Large-bean grade with strong visual and cup appeal',
    details: [
      'Structured acidity with a clean, premium finish',
      'Designed for feature offerings, private-label programs, and high-value wholesale lines',
      'Best suited for buyers who need a standout story without losing commercial relevance',
    ],
    buyerFit: 'Ideal for premium distributors seeking a flagship grade with marketable differentiation.',
  },
  {
    id: 'arabica',
    name: 'High-Altitude Arabica',
    subtitle: 'Balanced sweetness, clarity, and specialty-market versatility',
    details: [
      'Elevation-driven cup structure and cleaner flavor separation',
      'Strong fit for roasters, hospitality supply, and specialty retail channels',
      'Supports both single-origin storytelling and premium blending strategies',
    ],
    buyerFit: 'Ideal for importers and roasters looking for consistent specialty-grade character.',
  },
  {
    id: 'processing',
    name: 'Processing Profiles',
    subtitle: 'Handled for quality stability from cherry selection to lot prep',
    details: [
      'Selective harvesting, washing, drying, and grading workflow',
      'Attention to consistency before export conversations begin',
      'Built to help buyers compare lots with confidence and move faster on decisions',
    ],
    buyerFit: 'Ideal for wholesale teams that need clearer quality communication during sourcing.',
  },
]

/** @type {WorkflowStep[]} */
export const workflowSteps = [
  {
    id: 'selection',
    step: '01',
    title: 'Source Selection',
    copy: 'We start with high-potential lots and quality-forward farm relationships so the conversation begins with cup value, not commodity framing.',
  },
  {
    id: 'harvest',
    step: '02',
    title: 'Harvest & Sorting',
    copy: 'Only the right cherries move forward, which helps protect the quality expectations specialty buyers need later in the chain.',
  },
  {
    id: 'processing',
    step: '03',
    title: 'Processing & Drying',
    copy: 'Washing, fermentation, raised-bed drying, and grading steps are framed as quality controls, not decorative storytelling.',
  },
  {
    id: 'review',
    step: '04',
    title: 'Lot Review',
    copy: 'Lots are prepared for buyer conversations with clearer quality cues, profile alignment, and practical sourcing context.',
  },
  {
    id: 'export',
    step: '05',
    title: 'Export Coordination',
    copy: 'Documentation, commercial communication, and shipment readiness are positioned around what importers and distributors actually need to know.',
  },
  {
    id: 'distribution',
    step: '06',
    title: 'U.S. Market Alignment',
    copy: 'The final step is wholesale-fit messaging: pricing, buyer questions, sample planning, and the kind of story that works in the U.S. market.',
  },
]

/** @type {PartnerBenefit[]} */
export const partnerBenefits = [
  {
    id: 'sales',
    title: 'Sales-Ready Storytelling',
    copy: 'Your team gets a premium origin story that supports distributor sales conversations without drifting into retail-only language.',
    icon: 'line',
  },
  {
    id: 'buyers',
    title: 'Buyer-Centric Communication',
    copy: 'The messaging is written in U.S. English, shaped for wholesale expectations, and focused on the commercial big picture.',
    icon: 'briefcase',
  },
  {
    id: 'quality',
    title: 'Quality Without Noise',
    copy: 'The page emphasizes specialty quality, lot credibility, and sourcing clarity instead of packaging gimmicks or direct-to-consumer tropes.',
    icon: 'shield',
  },
  {
    id: 'growth',
    title: 'Partnership Positioning',
    copy: 'Everything is framed around helping importers, distributors, and specialty buyers build stronger premium coffee programs.',
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
    copy: 'A concise process narrative helps buyers understand how quality is protected before coffee reaches the U.S. market.',
  },
]

/** @type {GalleryItem[]} */
export const galleryItems = [
  {
    src: 'https://images.unsplash.com/photo-1762277142890-24902d58e8f0?auto=format&fit=crop&w=1600&q=80',
    alt: 'Hands holding freshly harvested coffee cherries',
    title: 'Harvest',
    description: 'Operational imagery that supports sourcing credibility and quality handling.',
  },
  {
    src: 'https://images.unsplash.com/photo-1761318543563-f5c211a99195?auto=format&fit=crop&w=1600&q=80',
    alt: 'Coffee beans drying outdoors during processing',
    title: 'Drying',
    description: 'The page should show process, not packaging theater.',
  },
  {
    src: 'https://images.unsplash.com/photo-1640770668482-8e3827119472?auto=format&fit=crop&w=1600&q=80',
    alt: 'Roasting drum filled with coffee beans',
    title: 'Roasting',
    description: 'A closer operational view of premium coffee handling after processing.',
  },
  {
    src: 'https://images.unsplash.com/photo-1703646617698-d61b240cd2f8?auto=format&fit=crop&w=1600&q=80',
    alt: 'Green coffee beans prepared for wholesale review',
    title: 'Green Coffee',
    description: 'Visual detail that supports lot conversations, profiling, and buyer review.',
  },
  {
    src: 'https://images.unsplash.com/photo-1569718974246-7b898eae87d3?auto=format&fit=crop&w=1600&q=80',
    alt: 'Coffee sacks staged in a warehouse for distribution',
    title: 'Distribution Readiness',
    description: 'Operational visuals reinforce the distributor-first positioning.',
  },
  {
    src: 'https://images.unsplash.com/photo-1650908007715-13db33e2de6c?auto=format&fit=crop&w=1600&q=80',
    alt: 'Coffee farm landscape with cultivated rows',
    title: 'Origin Depth',
    description: 'Kenyan highland origin appears as a subtle but credible quality layer.',
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
