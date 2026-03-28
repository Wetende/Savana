import { useEffect, useState } from 'react'
import { AnimatePresence, motion } from 'motion/react'
import { Clock3, Menu, MapPin, X } from 'lucide-react'

// Lucide dropped brand icons, so we provide lightweight inline SVGs matching lucide's style
const FacebookIcon = ({ size = 14 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>
)
const TwitterIcon = ({ size = 14 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"></path></svg>
)
const InstagramIcon = ({ size = 14 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
)
const YoutubeIcon = ({ size = 14 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"></path><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon></svg>
)

const MotionDiv = motion.div
const MotionNav = motion.nav

function Header({ links }) {
  const [menuOpen, setMenuOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => {
      setScrolled(window.scrollY > 28)
    }

    onScroll()
    window.addEventListener('scroll', onScroll)

    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    document.body.classList.toggle('menu-locked', menuOpen)

    return () => document.body.classList.remove('menu-locked')
  }, [menuOpen])

  const closeMenu = () => setMenuOpen(false)

  return (
    <div className={`header-overlay ${scrolled ? 'is-sticky' : ''}`}>
      <div className="topbar">
        <div className="shell-fluid topbar-inner" style={{ justifyContent: 'space-between' }}>
          <div className="topbar-item">
            <MapPin size={14} />
            <span>Global Sourcing</span>
          </div>
          
          <div className="topbar-socials">
            <a href="#facebook" aria-label="Facebook"><FacebookIcon size={14} /></a>
            <a href="#twitter" aria-label="Twitter"><TwitterIcon size={14} /></a>
            <a href="#instagram" aria-label="Instagram"><InstagramIcon size={14} /></a>
            <a href="#youtube" aria-label="YouTube"><YoutubeIcon size={14} /></a>
          </div>

          <div className="topbar-item">
            <Clock3 size={14} />
            <span>Open Monday to Friday</span>
          </div>
        </div>
      </div>

      <header className="site-header">
        <div className="shell-fluid header-inner">
          <a className="brand" href="#overview" aria-label="Savana Sips home">
            <span className="brand-mark">SS</span>
            <span className="brand-copy">
              <strong>Savana Sips</strong>
            </span>
          </a>

          <nav className="nav-desktop" aria-label="Primary navigation">
            {links.map((link) => (
              <div
                key={link.id}
                className={`nav-item ${link.dropdown ? 'has-dropdown' : ''}`}
              >
                <a href={link.href}>{link.label}</a>
                {link.dropdown && (
                  <div className="dropdown-menu">
                    {link.dropdown.map((subLink) => (
                      <a key={subLink.id} href={subLink.href}>
                        {subLink.label}
                      </a>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </nav>

          <div className="header-actions">
            <a className="button header-cta" href="#inquiry">
              Request Pricing
            </a>
            <button
              type="button"
              className="menu-toggle"
              aria-expanded={menuOpen}
              aria-label={menuOpen ? 'Close navigation' : 'Open navigation'}
              onClick={() => setMenuOpen((open) => !open)}
            >
              {menuOpen ? <X size={22} /> : <Menu size={22} />}
            </button>
          </div>
        </div>
      </header>

      <AnimatePresence>
        {menuOpen ? (
          <MotionDiv
            className="mobile-nav"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <MotionNav
              className="mobile-nav-panel"
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
              aria-label="Mobile navigation"
            >
              <div className="mobile-nav-top">
                <span className="brand-mark">SS</span>
                <button
                  type="button"
                  className="menu-toggle"
                  aria-label="Close navigation"
                  onClick={closeMenu}
                >
                  <X size={22} />
                </button>
              </div>

              <div className="mobile-nav-links">
                {links.map((link) => (
                  <div key={link.id}>
                    <a href={link.href} onClick={closeMenu}>
                      {link.label}
                    </a>
                    {link.dropdown && (
                      <div className="mobile-dropdown" style={{ paddingLeft: '1rem' }}>
                        {link.dropdown.map((subLink) => (
                          <a
                            key={subLink.id}
                            href={subLink.href}
                            onClick={closeMenu}
                            style={{ fontSize: '12px', borderBottom: 'none', padding: '0.5rem 0' }}
                          >
                            - {subLink.label}
                          </a>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              <a className="button button-primary mobile-nav-cta" href="#inquiry" onClick={closeMenu}>
                Request Pricing
              </a>
            </MotionNav>
          </MotionDiv>
        ) : null}
      </AnimatePresence>
    </div>
  )
}

export default Header
