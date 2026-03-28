import Lightbox from 'yet-another-react-lightbox'
import 'yet-another-react-lightbox/styles.css'

function GalleryLightbox({ items, openIndex, onClose, onOpen }) {
  return (
    <>
      <div className="gallery-grid">
        {items.map((item, index) => (
          <button
            type="button"
            key={item.src}
            className="gallery-card"
            aria-label={`View ${item.title} image`}
            onClick={() => onOpen(index)}
          >
            <img src={item.src} alt={item.alt} loading="lazy" />
            <span className="gallery-overlay">
              <strong>{item.title}</strong>
              <span>{item.description}</span>
            </span>
          </button>
        ))}
      </div>

      <Lightbox
        open={openIndex >= 0}
        close={onClose}
        index={openIndex}
        slides={items}
        controller={{ closeOnBackdropClick: true }}
      />
    </>
  )
}

export default GalleryLightbox
