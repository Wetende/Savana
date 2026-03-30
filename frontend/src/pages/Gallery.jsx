import { useState } from 'react'
import { Link } from 'react-router-dom'
import { galleryItems, galleryCategories } from '../content/siteContent.js'
import Reveal from '../components/Reveal.jsx'
import SectionHeading from '../components/SectionHeading.jsx'
import { Truck, Ship, Globe, ShieldCheck, ChevronRight } from 'lucide-react'
import Lightbox from "yet-another-react-lightbox"
import "yet-another-react-lightbox/styles.css"

export default function Gallery() {
  const [activeCategory, setActiveCategory] = useState('ALL')
  const [lightboxOpen, setLightboxOpen] = useState(false)
  const [lightboxIndex, setLightboxIndex] = useState(0)

  // Filter items
  const filteredItems = activeCategory === 'ALL' 
    ? galleryItems 
    : galleryItems.filter(item => item.category === activeCategory)

  // Mapping to lightbox format
  const slides = filteredItems.map(item => ({ src: item.src }))

  const openLightbox = (index) => {
    setLightboxIndex(index)
    setLightboxOpen(true)
  }

  return (
    <main style={{ minHeight: '100vh', backgroundColor: 'var(--back)', color: 'var(--text)' }}>
      
      {/* 1. Hero Banner */}
      <section style={{
        position: 'relative',
        height: '45vh',
        minHeight: '380px',
        width: '100%',
        backgroundImage: 'url(https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?auto=format&fit=crop&w=1920&q=80)',
        backgroundSize: 'cover',
        backgroundPosition: 'center 40%',
        backgroundAttachment: 'fixed',
        display: 'flex',
        alignItems: 'end',
      }}>
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'linear-gradient(to top, var(--back) 0%, rgba(10,10,12,0.6) 50%, rgba(0,0,0,0.8) 100%)',
          zIndex: 1
        }}></div>

        <div className="shell" style={{ position: 'relative', zIndex: 2, paddingBottom: '50px', width: '100%' }}>
          <Reveal>
            <h1 style={{
              fontSize: 'clamp(3rem, 7vw, 6rem)',
              color: '#fff',
              lineHeight: 1,
              fontWeight: '700',
              margin: 0,
              textTransform: 'uppercase',
              letterSpacing: '-1px'
            }}>
              Gallery
            </h1>
          </Reveal>
        </div>
      </section>

      {/* 2. Gallery Header & Filters */}
      <section className="section-shell" style={{ paddingTop: '80px', paddingBottom: '40px' }}>
        <div className="shell">
          <Reveal>
            <SectionHeading
              eyebrow="ORIGIN & OPERATIONS"
              title="Explore Our Facilities"
              align="center"
            />
          </Reveal>

          <Reveal delay={0.1}>
            <div style={{
              display: 'flex',
              flexWrap: 'wrap',
              justifyContent: 'center',
              gap: '15px',
              marginTop: '50px'
            }}>
              {galleryCategories.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setActiveCategory(cat)}
                  style={{
                    padding: '12px 28px',
                    backgroundColor: activeCategory === cat ? 'var(--gold)' : '#111214',
                    color: activeCategory === cat ? '#000' : 'var(--text-muted)',
                    border: 'none',
                    borderRadius: '4px',
                    fontSize: '13px',
                    fontWeight: '700',
                    letterSpacing: '1px',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    textTransform: 'uppercase'
                  }}
                  onMouseOver={(e) => {
                    if (activeCategory !== cat) {
                      e.currentTarget.style.backgroundColor = '#1a1b1e';
                      e.currentTarget.style.color = '#fff';
                    }
                  }}
                  onMouseOut={(e) => {
                    if (activeCategory !== cat) {
                      e.currentTarget.style.backgroundColor = '#111214';
                      e.currentTarget.style.color = 'var(--text-muted)';
                    }
                  }}
                >
                  {cat}
                </button>
              ))}
            </div>
          </Reveal>
        </div>
      </section>

      {/* 3. Image Grid */}
      <section className="section-shell" style={{ paddingTop: '20px', paddingBottom: '120px' }}>
        <div className="shell">
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
            gap: '30px'
          }}>
            {filteredItems.map((item, index) => (
              <Reveal delay={index * 0.05} key={item.title + index}>
                <div 
                  onClick={() => openLightbox(index)}
                  style={{
                    position: 'relative',
                    width: '100%',
                    aspectRatio: '1 / 1',
                    overflow: 'hidden',
                    cursor: 'pointer',
                    backgroundColor: '#111',
                    borderRadius: '0px'
                  }}
                  className="gallery-image-wrapper"
                >
                  <img 
                    src={item.src} 
                    alt={item.alt}
                    style={{
                      width: '100%',
                      height: '100%',
                      objectFit: 'cover',
                      transition: 'transform 0.5s ease'
                    }}
                    className="gallery-img"
                  />
                  <div className="gallery-hover-overlay" style={{
                    position: 'absolute',
                    inset: 0,
                    backgroundColor: 'rgba(196, 163, 119, 0.85)', // gold overlay
                    opacity: 0,
                    transition: 'opacity 0.3s ease',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                    padding: '20px',
                    textAlign: 'center'
                  }}>
                    <h3 style={{ color: '#fff', fontSize: '24px', marginBottom: '8px' }}>{item.title}</h3>
                    <p style={{ color: '#fff', fontSize: '14px', margin: 0 }}>View Full Image</p>
                  </div>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <Lightbox
        open={lightboxOpen}
        close={() => setLightboxOpen(false)}
        index={lightboxIndex}
        slides={slides}
      />

      <style>{`
        .gallery-image-wrapper:hover .gallery-img {
          transform: scale(1.1);
        }
        .gallery-image-wrapper:hover .gallery-hover-overlay {
          opacity: 1 !important;
        }
      `}</style>

      {/* 4. Wholesale CTA Banner */}
      <section style={{
        position: 'relative',
        padding: '120px 0',
        backgroundImage: 'url(https://images.unsplash.com/photo-1559525839-b184a4d698c7?auto=format&fit=crop&w=1920&q=80)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundAttachment: 'fixed',
      }}>
        <div style={{
          position: 'absolute',
          inset: 0,
          backgroundColor: 'rgba(10,10,12,0.85)'
        }}></div>

        <div className="shell" style={{ position: 'relative', zIndex: 2, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
          <Reveal>
            <span style={{ color: 'var(--gold)', letterSpacing: '2px', fontSize: '12px', textTransform: 'uppercase', display: 'block', marginBottom: '15px' }}>
              READY TO SECURE YOUR SUPPLY?
            </span>
            <h2 style={{ color: '#fff', fontSize: 'clamp(2rem, 5vw, 3.5rem)', marginBottom: '40px', maxWidth: '800px', lineHeight: 1.1 }}>
              Start a Wholesale Inquiry with Our Team
            </h2>
            <Link to="/#inquiry" className="button button-primary" style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '16px 40px', fontSize: '14px' }}>
              REQUEST PRICING <ChevronRight size={16} />
            </Link>
          </Reveal>
        </div>
      </section>

      {/* 5. Logistics Banner (Replacing Restaurant Logos) */}
      <section style={{
        backgroundColor: '#0a0a0c',
        padding: '60px 0',
        borderTop: '1px solid rgba(255,255,255,0.05)',
        borderBottom: '1px solid rgba(255,255,255,0.05)'
      }}>
        <div className="shell">
          <Reveal delay={0.2}>
            <div style={{
              display: 'flex',
              flexWrap: 'wrap',
              justifyContent: 'center',
              alignItems: 'center',
              gap: '60px',
              opacity: 0.5
            }}>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>
                <Globe size={40} strokeWidth={1} />
                <span style={{ fontSize: '11px', letterSpacing: '1px', textTransform: 'uppercase' }}>Global Export</span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>
                <ShieldCheck size={40} strokeWidth={1} />
                <span style={{ fontSize: '11px', letterSpacing: '1px', textTransform: 'uppercase' }}>Certified Grade</span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>
                <Truck size={40} strokeWidth={1} />
                <span style={{ fontSize: '11px', letterSpacing: '1px', textTransform: 'uppercase' }}>Port Delivery</span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>
                <Ship size={40} strokeWidth={1} />
                <span style={{ fontSize: '11px', letterSpacing: '1px', textTransform: 'uppercase' }}>Ocean Freight</span>
              </div>
            </div>
          </Reveal>
        </div>
      </section>
    </main>
  )
}
