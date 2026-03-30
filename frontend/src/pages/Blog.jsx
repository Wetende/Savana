import { Link } from 'react-router-dom'
import { blogPosts } from '../content/siteContent.js'
import Reveal from '../components/Reveal.jsx'
import SectionHeading from '../components/SectionHeading.jsx'
import { Calendar, ChevronRight } from 'lucide-react'

export default function Blog() {
  return (
    <main className="section-shell" style={{ paddingTop: '160px', minHeight: '100vh', paddingBottom: '100px' }}>
      <div className="shell">
        <Reveal>
          <SectionHeading
            eyebrow="Market Insights"
            title="Savana Sips Journal"
            align="center"
          />
        </Reveal>

        <div className="blog-grid" style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: '30px',
          marginTop: '60px'
        }}>
          {blogPosts.map((post, index) => (
            <Reveal className="blog-card" delay={index * 0.1} key={post.id} style={{
              position: 'relative',
              borderRadius: '0px', // Assuming square edges per Kaffen theme, adjust if needed
              overflow: 'hidden',
              display: 'flex',
              flexDirection: 'column',
              boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
              height: '400px',
              backgroundColor: '#111'
            }}>
              {/* Background Image */}
              <div style={{
                position: 'absolute',
                inset: 0,
                backgroundImage: `url(${post.image})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                transition: 'transform 0.5s ease',
                zIndex: 1
              }} className="blog-card-bg" />

              {/* Gradient Overlay */}
              <div style={{
                position: 'absolute',
                inset: 0,
                background: 'linear-gradient(to top, rgba(10,10,12,0.95) 0%, rgba(10,10,12,0.6) 40%, transparent 100%)',
                zIndex: 2
              }} />

              {/* Content Box */}
              <div className="blog-card-content" style={{ 
                position: 'relative',
                zIndex: 3,
                padding: '30px', 
                display: 'flex', 
                flexDirection: 'column', 
                flexGrow: 1,
                justifyContent: 'flex-end'
              }}>
                <h3 style={{ 
                  fontSize: '22px', 
                  lineHeight: '1.3', 
                  marginBottom: '16px',
                  fontWeight: '600',
                  color: '#fff'
                }}>
                  <Link to={`/blog/${post.id}`} style={{ color: 'inherit', textDecoration: 'none' }} className="hover-gold">
                    {post.title}
                  </Link>
                </h3>
                
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '20px', 
                  color: '#aaa', 
                  fontSize: '13px',
                  marginTop: '4px'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Calendar size={14} color="#aaa" />
                    <span>{post.date}</span>
                  </div>

                  <Link to={`/blog/${post.id}`} style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: '4px',
                    color: '#aaa',
                    textDecoration: 'none',
                    transition: 'color 0.3s ease'
                  }} className="hover-gold">
                    <ChevronRight size={14} color="#aaa" />
                    <span>Read More</span>
                  </Link>
                </div>
              </div>

              {/* Hover effect targeting the background */}
              <style>{`
                .blog-card:hover .blog-card-bg {
                  transform: scale(1.05);
                }
                .hover-gold:hover {
                  color: var(--gold) !important;
                }
                .hover-gold:hover svg {
                  stroke: var(--gold) !important;
                }
              `}</style>
            </Reveal>
          ))}
        </div>
      </div>
    </main>
  )
}
