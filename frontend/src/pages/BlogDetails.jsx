import { useParams, Link } from 'react-router-dom'
import { blogPosts } from '../content/siteContent.js'
import { ChevronLeft } from 'lucide-react'

export default function BlogDetails() {
  const { id } = useParams()
  const post = blogPosts.find(p => p.id === id)

  if (!post) {
    return (
      <main className="section-shell" style={{ paddingTop: '200px', minHeight: '100vh', textAlign: 'center' }}>
        <h2>Post Not Found</h2>
        <Link to="/blog" style={{ color: 'var(--gold)', marginTop: '20px', display: 'inline-block' }}>
          Return to Blog
        </Link>
      </main>
    )
  }

  return (
    <main style={{ minHeight: '100vh', backgroundColor: 'var(--back)', color: 'var(--text)' }}>
      {/* Detail Container */}
      <section className="section-shell" style={{ paddingTop: '160px', paddingBottom: '120px' }}>
        <div className="shell" style={{ maxWidth: '800px', margin: '0 auto' }}>
          
          <Link to="/blog" style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px',
            color: 'var(--gold)',
            textTransform: 'uppercase',
            fontSize: '13px',
            fontWeight: '600',
            letterSpacing: '1px',
            marginBottom: '40px',
            textDecoration: 'none'
          }}>
            <ChevronLeft size={16} /> Back to Journal
          </Link>

          {/* Title */}
          <h1 style={{
            fontSize: 'clamp(2rem, 4vw, 3rem)',
            color: '#fff',
            lineHeight: 1.2,
            marginBottom: '30px',
            fontWeight: '600'
          }}>
            {post.title}
          </h1>

          {/* Featured Image */}
          <img 
            src={post.image} 
            alt={post.title} 
            style={{
              width: '100%',
              height: 'auto',
              maxHeight: '500px',
              objectFit: 'cover',
              marginBottom: '40px',
              display: 'block'
            }} 
          />

          {/* Rich Content Area */}
          <div 
            className="rich-text-content"
            style={{
              fontSize: '16px',
              lineHeight: 1.8,
              color: '#8b8b91', // Muted gray matching Kaffen text paragraphs
            }}
            dangerouslySetInnerHTML={{ __html: post.content }}
          />

          {/* Blog Detail Scoped Styles */}
          <style>{`
            .rich-text-content p {
              margin-bottom: 24px;
            }
            
            .rich-text-content blockquote {
              background-color: #121315; /* Slightly darker/different shade for blockquote */
              padding: 40px;
              margin: 40px 0;
              border-radius: 4px;
            }

            .rich-text-content blockquote p {
              font-size: 22px;
              color: #ffffff;
              line-height: 1.5;
              margin-bottom: 20px;
              font-style: italic;
            }

            .rich-text-content blockquote cite {
              display: flex;
              align-items: center;
              font-size: 14px;
              color: #fff;
              font-style: normal;
            }

            .rich-text-content blockquote cite::before {
              content: '';
              display: inline-block;
              width: 30px;
              height: 2px;
              background-color: var(--gold);
              margin-right: 15px;
            }

            .rich-text-content ul {
              margin: 30px 0;
              padding-left: 20px;
            }

            .rich-text-content li {
              position: relative;
              padding-left: 15px;
              margin-bottom: 12px;
              list-style: none; /* We remove default bullet because Kaffen uses custom bullet */
              color: #fff;
            }

            .rich-text-content li::before {
              content: '';
              position: absolute;
              left: -5px;
              top: 10px;
              width: 5px;
              height: 5px;
              border-radius: 50%;
              background-color: #fff;
            }
          `}</style>

          <div style={{
            marginTop: '80px',
            paddingTop: '40px',
            borderTop: '1px solid rgba(255,255,255,0.05)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <Link to="/blog" className="button button-outline" style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
              <ChevronLeft size={16} /> More Articles
            </Link>
          </div>
        </div>
      </section>
    </main>
  )
}
