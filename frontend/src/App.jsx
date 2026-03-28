import { useState } from 'react'
import {
  BadgeCheck,
  BriefcaseBusiness,
  Container,
  Leaf,
  ShieldCheck,
  TimerReset,
  TrendingUp,
  Ship,
} from 'lucide-react'
import Header from './components/Header.jsx'
import HeroSlider from './components/HeroSlider.jsx'
import Reveal from './components/Reveal.jsx'
import SectionHeading from './components/SectionHeading.jsx'
import GalleryLightbox from './components/GalleryLightbox.jsx'
import InquiryForm from './components/InquiryForm.jsx'
import {
  coffeeSpecs,
  galleryItems,
  heroSlides,
  impactStats,
  navLinks,
  partnerBenefits,
  trustPoints,
  workflowSteps,
} from './content/siteContent.js'

const iconMap = {
  badge: BadgeCheck,
  container: Container,
  leaf: Leaf,
  timer: TimerReset,
  line: TrendingUp,
  briefcase: BriefcaseBusiness,
  shield: ShieldCheck,
  ship: Ship,
}

function App() {
  const [lightboxIndex, setLightboxIndex] = useState(-1)

  return (
    <div className="site-shell">
      <Header links={navLinks} />

      <main>
        <HeroSlider slides={heroSlides} />

        <section className="trust-band">
          <div className="shell trust-grid">
            {trustPoints.map((point, index) => {
              const Icon = iconMap[point.icon]

              return (
                <Reveal className="trust-card" delay={index * 0.08} key={point.id}>
                  <span className="trust-icon">
                    <Icon size={18} />
                  </span>
                  <h3>{point.title}</h3>
                  <p>{point.description}</p>
                </Reveal>
              )
            })}
          </div>
        </section>

        <section id="market-position" className="section-shell section-story">
          <div className="shell two-column">
            <Reveal>
              <SectionHeading
                eyebrow="Who We Are"
                title="Premium specialty coffee for the U.S. wholesale market"
                description="Savana Sips partners with U.S. importers, roasters, and distributors who want consistent specialty-grade coffee backed by full supply-chain transparency and dedicated sourcing support."
              />
            </Reveal>

            <Reveal className="story-panel" delay={0.12}>
              <p>
                We focus on one thing: connecting U.S. buyers with exceptional coffee that performs
                in their programs. Every lot is selected for cup quality, graded for consistency,
                and prepared with export-ready documentation.
              </p>
              <ul className="story-list">
                <li>Dedicated wholesale account management</li>
                <li>Specialty-grade sourcing with full traceability</li>
                <li>Flexible lot sizes for distributors of every scale</li>
              </ul>
            </Reveal>
          </div>
        </section>

        <section id="coffee-specs" className="section-shell section-specs">
          <div className="shell">
            <Reveal>
              <SectionHeading
                eyebrow="Coffee Specs"
                title="Specialty-grade profiles for premium wholesale programs"
                description="From high-altitude AA selections to carefully processed Arabica lots, each profile is built for repeat commercial performance in premium channels."
              />
            </Reveal>

            <div className="spec-grid">
              {coffeeSpecs.map((spec, index) => (
                <Reveal className="spec-card" delay={index * 0.08} key={spec.id}>
                  <p className="spec-kicker">{spec.subtitle}</p>
                  <h3>{spec.name}</h3>
                  <ul>
                    {spec.details.map((detail) => (
                      <li key={detail}>{detail}</li>
                    ))}
                  </ul>
                  <p className="spec-fit">{spec.buyerFit}</p>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        <section id="sourcing" className="section-shell section-workflow">
          <div className="shell">
            <Reveal>
              <SectionHeading
                eyebrow="Farm to Export"
                title="From cherry to shipment, quality at every step"
                description="Our six-step sourcing workflow ensures every lot meets specialty standards before it reaches your warehouse."
              />
            </Reveal>

            <div className="workflow-grid">
              {workflowSteps.map((step, index) => (
                <Reveal className="workflow-card" delay={index * 0.06} key={step.id}>
                  <span className="workflow-step">{step.step}</span>
                  <h3>{step.title}</h3>
                  <p>{step.copy}</p>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        <section id="distribution" className="section-shell section-benefits">
          <div className="shell benefits-layout">
            <Reveal className="benefits-copy">
              <SectionHeading
                eyebrow="Why Partner with Savana Sips"
                title="Built for serious wholesale partnerships"
                description="Everything we do centers on making your buying process smoother — from first inquiry to recurring supply. Quality coffee, reliable sourcing, clear communication."
              />
              <div className="quote-panel">
                <p>
                  "The best wholesale relationships start with a shared commitment to quality and
                  transparency. That's how we operate."
                </p>
              </div>
            </Reveal>

            <div className="benefit-grid">
              {partnerBenefits.map((benefit, index) => {
                const Icon = iconMap[benefit.icon]

                return (
                  <Reveal className="benefit-card" delay={index * 0.08} key={benefit.id}>
                    <span className="benefit-icon">
                      <Icon size={18} />
                    </span>
                    <h3>{benefit.title}</h3>
                    <p>{benefit.copy}</p>
                  </Reveal>
                )
              })}
            </div>
          </div>
        </section>

        <section id="impact" className="section-shell section-impact">
          <div className="shell impact-layout">
            <Reveal>
              <SectionHeading
                eyebrow="Impact & Ethical Sourcing"
                title="Origin credibility that supports premium positioning"
                description="Fair compensation for farmers, sustainable practices at every stage, and full traceability — because long-term supply quality starts at the source."
              />
            </Reveal>

            <div className="impact-grid">
              {impactStats.map((stat, index) => (
                <Reveal className="impact-card" delay={index * 0.08} key={stat.id}>
                  <strong>{stat.value}</strong>
                  <h3>{stat.label}</h3>
                  <p>{stat.copy}</p>
                </Reveal>
              ))}
            </div>

            <Reveal className="impact-banner" delay={0.16}>
              <p>
                Our highland Kenyan lots bring distinctive cup character that adds genuine
                market distinction to your catalog — backed by transparent sourcing from
                cooperatives we have worked with for years.
              </p>
            </Reveal>
          </div>
        </section>

        <section className="section-shell section-gallery">
          <div className="shell">
            <Reveal>
              <SectionHeading
                eyebrow="Operational Gallery"
                title="From farm to warehouse, quality you can see"
                description="A closer look at our sourcing, processing, and distribution operations — because transparency builds trust."
              />
            </Reveal>

            <Reveal delay={0.12}>
              <GalleryLightbox
                items={galleryItems}
                openIndex={lightboxIndex}
                onClose={() => setLightboxIndex(-1)}
                onOpen={setLightboxIndex}
              />
            </Reveal>
          </div>
        </section>

        <section id="inquiry" className="section-shell section-inquiry">
          <div className="shell inquiry-layout">
            <Reveal className="inquiry-copy">
              <SectionHeading
                eyebrow="Wholesale Inquiry"
                title="Start the pricing and supply conversation"
                description="Use the form to request wholesale pricing, share your buyer profile, and open a conversation around volume, quality fit, and lot availability."
              />

              <div className="inquiry-list">
                <div>
                  <strong>Best for</strong>
                  <span>Importers, distributors, specialty roasters, hospitality supply groups</span>
                </div>
                <div>
                  <strong>Primary ask</strong>
                  <span>Pricing, coffee specs, sample discussions, and sourcing alignment</span>
                </div>
                <div>
                  <strong>Message style</strong>
                  <span>U.S.-market commercial language with premium origin credibility</span>
                </div>
              </div>
            </Reveal>

            <Reveal className="inquiry-panel" delay={0.12}>
              <InquiryForm />
            </Reveal>
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <div className="shell footer-grid">
          <div>
            <a className="brand footer-brand" href="#overview">
              <span className="brand-mark">SS</span>
              <span className="brand-copy">
                <strong>Savana Sips</strong>
                <span>Premium Coffee Supply for U.S. Wholesale Buyers</span>
              </span>
            </a>
          </div>

          <nav className="footer-links" aria-label="Footer navigation">
            {navLinks.map((link) => (
              <a key={link.id} href={link.href}>
                {link.label}
              </a>
            ))}
          </nav>

          <p className="footer-note">
            © 2026 Savana Sips. Premium Specialty Coffee Supply.
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
