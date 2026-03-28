import { useState } from 'react'
import Reveal from './Reveal.jsx'
import SectionHeading from './SectionHeading.jsx'
import GalleryLightbox from './GalleryLightbox.jsx'
import { galleryItems } from '../content/siteContent.js'

export default function OperationalGallery() {
  const [lightboxIndex, setLightboxIndex] = useState(-1)

  return (
    <section className="section-shell section-gallery">
      <div className="shell">
        <Reveal>
          <SectionHeading
            eyebrow="Operational Gallery"
            title="From farm to warehouse, quality you can see"
            description="A closer look at our sourcing, processing, and distribution operations — because transparency builds trust."
            align="center"
          />
        </Reveal>

        <Reveal delay={0.12}>
          <GalleryLightbox
            items={galleryItems}
            openIndex={lightboxIndex}
            onClose={() => setLightboxIndex(-1)}
            onOpen={setLightboxIndex}
          />
        </Reveal>
      </div>
    </section>
  )
}
