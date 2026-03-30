import { Routes, Route, useLocation } from 'react-router-dom'
import { useEffect } from 'react'
import Header from './components/Header.jsx'
import Home from './pages/Home.jsx'
import Blog from './pages/Blog.jsx'
import BlogDetails from './pages/BlogDetails.jsx'
import Gallery from './pages/Gallery.jsx'
import { navLinks } from './content/siteContent.js'
import { MapPin, Mail, Phone } from 'lucide-react'

// Scroll to top on route change or to hash
function ScrollToTop() {
  const { pathname, hash } = useLocation();

  useEffect(() => {
    if (hash) {
      setTimeout(() => {
        const id = hash.replace('#', '');
        const element = document.getElementById(id);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    } else {
      window.scrollTo(0, 0);
    }
  }, [pathname, hash]);

  return null;
}

function App() {
  return (
    <div className="site-shell">
      <ScrollToTop />
      <Header links={navLinks} />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/gallery" element={<Gallery />} />
        <Route path="/blog" element={<Blog />} />
        <Route path="/blog/:id" element={<BlogDetails />} />
      </Routes>

      <footer className="site-footer">
        <div className="shell footer-columns">
          <div className="footer-col footer-col-brand">
            <a className="brand footer-brand" href="/#overview">
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
              <a href="/#inquiry">Wholesale Inquiry</a>
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
