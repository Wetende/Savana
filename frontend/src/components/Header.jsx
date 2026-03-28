import { useEffect, useState } from 'react'
import { AnimatePresence, motion } from 'motion/react'
import { Clock3, Menu, ShipWheel, X } from 'lucide-react'

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
    <>
      <div className="topbar">
        <div className="shell topbar-inner">
          <div className="topbar-item">
            <ShipWheel size={14} />
            <span>Built for U.S. distributors, importers, and specialty buyers</span>
          </div>
          <div className="topbar-item">
            <Clock3 size={14} />
            <span>Wholesale responses focused on pricing, specs, and lot availability</span>
          </div>
        </div>
      </div>

      <header className={`site-header ${scrolled ? 'is-scrolled' : ''}`}>
        <div className="shell header-inner">
          <a className="brand" href="#overview" aria-label="Savana Sips home">
            <span className="brand-mark">SS</span>
            <span className="brand-copy">
              <strong>Savana Sips</strong>
              <span>Wholesale Coffee Supply</span>
            </span>
          </a>

          <nav className="nav-desktop" aria-label="Primary navigation">
            {links.map((link) => (
              <a key={link.id} href={link.href}>
                {link.label}
              </a>
            ))}
          </nav>

          <div className="header-actions">
            <a className="button button-outline header-cta" href="#coffee-specs">
              View Coffee Specs
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
                  <a key={link.id} href={link.href} onClick={closeMenu}>
                    {link.label}
                  </a>
                ))}
              </div>

              <a className="button button-primary mobile-nav-cta" href="#inquiry" onClick={closeMenu}>
                Request Wholesale Pricing
              </a>
            </MotionNav>
          </MotionDiv>
        ) : null}
      </AnimatePresence>
    </>
  )
}

export default Header
