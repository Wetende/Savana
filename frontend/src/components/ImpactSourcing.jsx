import Reveal from './Reveal.jsx'
import SectionHeading from './SectionHeading.jsx'
import { impactStats } from '../content/siteContent.js'

export default function ImpactSourcing() {
  return (
    <section id="impact" className="section-shell section-impact">
      <div className="shell impact-layout">
        <Reveal>
          <SectionHeading
            eyebrow="Impact & Ethical Sourcing"
            title="Origin credibility that supports premium positioning"
            description="Fair compensation for farmers, sustainable practices at every stage, and full traceability — because long-term supply quality starts at the source."
            align="center"
          />
        </Reveal>

        <div className="impact-list">
          {impactStats.map((stat, index) => (
            <Reveal className="impact-list-item" delay={index * 0.08} key={stat.id}>
              <strong>{stat.value}</strong>
              <div className="impact-content">
                <h3>{stat.label}</h3>
                <p>{stat.copy}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}
