import { useState } from 'react'
import {
  BadgeCheck,
  BriefcaseBusiness,
  Container,
  Coffee,
  Leaf,
  MapPin,
  ShieldCheck,
  Sun,
  TimerReset,
  TrendingUp,
  Truck,
  Ship,
  ChevronRight,
  Star,
  Mail,
  Phone,
  Clock,
} from 'lucide-react'
import Header from './components/Header.jsx'
import HeroSlider from './components/HeroSlider.jsx'
import Reveal from './components/Reveal.jsx'
import SectionHeading from './components/SectionHeading.jsx'
import InquiryForm from './components/InquiryForm.jsx'
import AboutUs from './components/AboutUs.jsx'
// import OperationalGallery from './components/OperationalGallery.jsx'

import {
  coffeeSpecs,
  heroSlides,
  navLinks,
  partnerBenefits,
  trustPoints,
  workflowSteps,
  companyStats,
  testimonials,
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
  MapPin: MapPin,
  Leaf: Leaf,
  Sun: Sun,
  Truck: Truck,
}

function App() {
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

        <AboutUs />

        <section id="coffee-specs" className="section-shell section-specs">
          <div className="bg-decoration bg-decoration-1">
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <path d="M50,0 C80,0 100,20 100,50 C100,80 80,100 50,100 C20,100 0,80 0,50 C0,20 20,0 50,0 Z M50,10 C25,10 10,25 10,50 C10,75 25,90 50,90 C75,90 90,75 90,50 C90,25 75,10 50,10 Z" />
            </svg>
          </div>
          <div className="bg-decoration bg-decoration-2">
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <path d="M50,0 C60,0 80,10 90,30 C100,50 90,80 70,90 C50,100 20,90 10,70 C0,50 10,20 30,10 C40,5 45,0 50,0 Z M50,90 C70,90 90,70 90,50 C90,30 70,10 50,10 C30,10 10,30 10,50 C10,70 30,90 50,90 Z" />
            </svg>
          </div>
          <div className="shell">
            <Reveal>
              <SectionHeading
                eyebrow="Our Coffees"
                title="Savana Sips Coffee Selection"
                align="center"
              />
            </Reveal>

            <div className="menu-container">
              <div className="menu-grid">
                {coffeeSpecs.map((spec, index) => (
                  <Reveal className="menu-item" delay={index * 0.08} key={spec.id}>
                    <div className="menu-item-image">
                      <img src={spec.image} alt={spec.name} />
                    </div>
                    <div className="menu-item-content">
                      <div className="menu-item-header">
                        <h3 className="menu-item-title">{spec.name}</h3>
                        <p className="menu-item-desc">{spec.subtitle}</p>
                      </div>
                      
                      <div className="menu-price-row">
                        <span className="menu-item-dots" />
                        <span className="menu-item-price">{spec.price}</span>
                      </div>
                    </div>
                  </Reveal>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section id="sourcing" className="section-shell section-workflow">
          <div className="shell about-kaffen-layout">
            <Reveal className="about-kaffen-content">
              <SectionHeading
                eyebrow="Farm to Export"
                title="From cherry to shipment, quality at every step"
                align="left"
              />
              <p className="about-kaffen-desc">
                High-potential green coffee sourcing requires precision. We manage the entire chain—from cherry selection to dry milling and export coordination—so your sourcing conversations focus entirely on cup quality and reliability.
              </p>
              
              <div className="about-feature-block">
                <div className="feature-icon-wrap">
                  <Coffee size={32} />
                </div>
                <div className="feature-text">
                  <h4>100% Export Grade</h4>
                  <p>Meticulous sorting and preparation for specialty buyers</p>
                </div>
              </div>

              <a className="button button-primary" href="#inquiry" style={{ marginTop: '30px' }}>
                START SOURCING <ChevronRight size={18} style={{ marginLeft: '4px', verticalAlign: 'middle' }} />
              </a>
            </Reveal>

            <div className="sourcing-offset-grid">
              {workflowSteps.map((step, index) => {
                const Icon = iconMap[step.icon]
                return (
                  <Reveal className="workflow-card-staggered" delay={index * 0.12} key={step.id}>
                    <div className="workflow-icon-badge">
                      <Icon size={36} />
                    </div>
                    <h3>{step.title}</h3>
                    <p>{step.copy}</p>
                  </Reveal>
                )
              })}
            </div>
          </div>
        </section>

        <section id="distribution" className="section-shell section-whychoose">
          <div className="shell whychoose-layout">
            <Reveal className="whychoose-image-col">
              <img
                src="https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=800&q=80"
                alt="Specialty coffee preparation"
                className="whychoose-image"
              />
              <div className="whychoose-floating-quote">
                <img 
                  src="https://images.unsplash.com/photo-1531384441138-2736e62e0919?auto=format&fit=crop&w=200&q=80" 
                  alt="CEO placeholder" 
                />
                <p>
                  "Our mission is to bridge the gap between dedicated Kenyan producers and the world's most uncompromising roasters."
                </p>
              </div>
            </Reveal>

            <Reveal className="whychoose-text-col" delay={0.12}>
              <SectionHeading
                eyebrow="Why Choose Us"
                title="Your trusted coffee partner"
                description="We make sourcing simple — great coffee, clear pricing, and reliable supply every time."
              />

              <div className="whychoose-features">
                {partnerBenefits.map((benefit) => {
                  const Icon = iconMap[benefit.icon]
                  return (
                    <div className="whychoose-feature" key={benefit.id}>
                      <span className="whychoose-feature-icon">
                        <Icon size={24} />
                      </span>
                      <div>
                        <h3>{benefit.title}</h3>
                        <p>{benefit.copy}</p>
                      </div>
                    </div>
                  )
                })}
              </div>

              <a className="button button-primary" href="#inquiry">
                Explore More
              </a>
            </Reveal>
          </div>
        </section>



        {/* 
          NOTE: The Operational Gallery section has been moved to its own component (src/components/OperationalGallery.jsx). 
          It is currently hidden per client request. Uncomment the line below to restore it to the landing page.
          
          <OperationalGallery /> 
        */}

        <section className="section-shell section-stats">
          <div className="bg-decoration" style={{ top: '-10%', right: '-5%', opacity: 0.04 }}>
            <svg width="400" height="400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
              <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1.8 9.2A7 7 0 0 1 11 20Z"></path>
              <path d="M11 20v-5"></path>
              <path d="M11 15c0-1-2.5-2-2.5-2S6 12 6 11"></path>
              <path d="M11 15c0-1 2.5-2 2.5-2S16 12 16 11"></path>
              <path d="M11 18c0-1-1.5-1.5-1.5-1.5S8 16 8 15.5"></path>
              <path d="M11 18c0-1 1.5-1.5 1.5-1.5S14 16 14 15.5"></path>
            </svg>
          </div>
          <div className="shell">
            <div className="stats-grid">
              {companyStats.map((stat, index) => {
                const Icon = iconMap[stat.icon] || Star
                return (
                  <Reveal className="stats-card" delay={index * 0.08} key={stat.id}>
                    <div className="stats-icon-wrap">
                      <Icon size={28} />
                    </div>
                    <strong>{stat.value}</strong>
                    <h3>{stat.label}</h3>
                    <p>{stat.copy}</p>
                  </Reveal>
                )
              })}
            </div>
          </div>
        </section>

        <section className="section-shell section-testimonials">
          <div className="shell">
            <Reveal>
              <SectionHeading
                eyebrow="CUSTOMER FEEDBACK"
                title="What Our Clients Say"
                align="center"
              />
            </Reveal>

            <div className="testimonial-grid">
              {testimonials.map((test, index) => (
                <Reveal className="testimonial-card" delay={index * 0.12} key={test.id}>
                  <div className="testimonial-avatar">
                    <img src={test.avatar} alt={test.name} />
                  </div>
                  <div className="testimonial-stars">
                    {[...Array(test.stars)].map((_, i) => (
                      <Star key={i} size={14} fill="var(--gold)" color="var(--gold)" />
                    ))}
                  </div>
                  <p className="testimonial-copy">{test.copy}</p>
                  <h4 className="testimonial-name">{test.name}</h4>
                  <span className="testimonial-role">{test.role}</span>
                </Reveal>
              ))}
            </div>
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
        <div className="shell footer-columns">
          <div className="footer-col footer-col-brand">
            <a className="brand footer-brand" href="#overview">
              <span className="brand-mark">SS</span>
              <span className="brand-copy">
                <strong>Savana Sips</strong>
                <span>Premium Coffee Supply</span>
              </span>
            </a>
            <p className="footer-tagline">
              Specialty-grade Kenyan coffee for wholesale buyers across North America and Europe. Origin-led quality, export-ready logistics.
            </p>
          </div>

          <div className="footer-col">
            <h4 className="footer-col-title">Working Hours</h4>
            <ul className="footer-hours">
              <li>
                <span className="footer-hours-day">Monday – Friday</span>
                <span className="footer-hours-time">08:00 am – 06:00 pm</span>
              </li>
              <li>
                <span className="footer-hours-day">Saturday</span>
                <span className="footer-hours-time">09:00 am – 01:00 pm</span>
              </li>
              <li className="footer-hours-closed">Sunday Closed</li>
            </ul>
          </div>

          <div className="footer-col">
            <h4 className="footer-col-title">Contact Us</h4>
            <ul className="footer-contact">
              <li>
                <MapPin size={16} className="footer-contact-icon" />
                <div>
                  <span className="footer-contact-label">Location :</span>
                  <span>Nairobi, Kenya</span>
                </div>
              </li>
              <li>
                <Mail size={16} className="footer-contact-icon" />
                <div>
                  <span className="footer-contact-label">Email Address :</span>
                  <span>hello@savanasips.com</span>
                </div>
              </li>
              <li>
                <Phone size={16} className="footer-contact-icon" />
                <div>
                  <span className="footer-contact-label">Phone Number :</span>
                  <span>+254 700 123 456</span>
                </div>
              </li>
            </ul>
          </div>

          <div className="footer-col">
            <h4 className="footer-col-title">Quick Links</h4>
            <nav className="footer-nav-links" aria-label="Footer navigation">
              {navLinks.map((link) => (
                <a key={link.id} href={link.href}>
                  {link.label}
                </a>
              ))}
              <a href="#inquiry">Wholesale Inquiry</a>
            </nav>
          </div>
        </div>

        <div className="footer-bottom">
          <div className="shell">
            <p className="footer-note">
              © 2026 Savana Sips. All Rights Reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
