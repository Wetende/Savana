import Reveal from './Reveal.jsx'
import SectionHeading from './SectionHeading.jsx'
import ImpactSourcing from './ImpactSourcing.jsx'

export default function AboutUs() {
  return (
    <>
      <section id="market-position" className="section-shell section-about">
        <div className="shell about-layout">
          <Reveal className="about-image-col">
            <div className="about-image-stack">
              <img
                src="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=800&q=80"
                alt="Barista preparing specialty coffee"
                className="about-image"
              />
            </div>
            <div className="about-quote-box">
              <p>
                "The best wholesale relationships start with a shared commitment to quality and
                transparency. That's how we operate."
              </p>
            </div>
          </Reveal>

          <Reveal className="about-text-col" delay={0.12}>
            <SectionHeading
              eyebrow="About Us"
              title="Premium specialty coffee for the U.S. wholesale market"
              description="Savana Sips partners with U.S. importers, roasters, and distributors who want consistent specialty-grade coffee backed by full supply-chain transparency and dedicated sourcing support."
            />
            <p className="about-body">
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

      {/* <ImpactSourcing /> */}
    </>
  )
}
