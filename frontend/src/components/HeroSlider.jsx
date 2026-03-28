import { useState } from 'react'
import { ChevronRight, ChartColumnIncreasing, ShieldCheck } from 'lucide-react'
import { useReducedMotion } from 'motion/react'
import { A11y, Autoplay, EffectFade, Pagination } from 'swiper/modules'
import { Swiper, SwiperSlide } from 'swiper/react'
import SplitHeadline from './SplitHeadline.jsx'

import 'swiper/css'
import 'swiper/css/effect-fade'
import 'swiper/css/pagination'

function HeroSlider({ slides }) {
  const reduceMotion = useReducedMotion()
  const [activeIndex, setActiveIndex] = useState(0)

  return (
    <section id="overview" className="hero-section">
      <Swiper
        className="hero-swiper"
        modules={[A11y, Autoplay, EffectFade, Pagination]}
        effect="fade"
        speed={reduceMotion ? 0 : 900}
        autoplay={
          reduceMotion
            ? false
            : {
                delay: 6800,
                disableOnInteraction: false,
              }
        }
        pagination={{ clickable: true, el: '.hero-pagination' }}
        onSlideChange={(swiper) => setActiveIndex(swiper.realIndex)}
      >
        {slides.map((slide, index) => {
          const active = activeIndex === index

          return (
            <SwiperSlide key={slide.id}>
              <div className="hero-slide">
                <div
                  className="hero-media"
                  style={{ backgroundImage: `url(${slide.image})` }}
                />

                <div className="shell hero-grid">
                  <div className="hero-copy">
                    <p className="eyebrow">{slide.eyebrow}</p>
                    <SplitHeadline text={slide.title} active={active} />

                    <div className="hero-actions">
                      <a className="button button-primary" href="#inquiry">
                        Request Pricing
                        <ChevronRight size={16} />
                      </a>
                      <a className="button button-outline" href="#coffee-specs">
                        Our Coffees
                        <ChevronRight size={16} />
                      </a>
                    </div>
                  </div>

                  <aside className="hero-aside" style={{ display: 'none' }}>
                    <div className="hero-note">
                      <span className="hero-note-icon">
                        <ShieldCheck size={18} />
                      </span>
                      <p>{slide.highlight}</p>
                    </div>

                    <div className="hero-card">
                      <div className="hero-card-header">
                        <ChartColumnIncreasing size={18} />
                        <span>Wholesale Positioning</span>
                      </div>
                      <h3>Built for premium supply conversations</h3>
                      <p>
                        The site leads with quality, traceability, and distributor value so U.S.
                        buyers immediately understand the commercial case.
                      </p>
                    </div>
                  </aside>
                </div>
              </div>
            </SwiperSlide>
          )
        })}
      </Swiper>

      <div className="shell hero-bottom">
        <div className="hero-pagination" />
      </div>
    </section>
  )
}

export default HeroSlider
