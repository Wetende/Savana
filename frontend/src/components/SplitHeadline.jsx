import { useReducedMotion } from 'motion/react'

function SplitHeadline({ text, active }) {
  const reduceMotion = useReducedMotion()

  if (reduceMotion) {
    return <h1 className="hero-title">{text}</h1>
  }

  let charIndex = 0
  const words = text.split(' ')

  return (
    <h1 className={`hero-title ${active ? 'is-active' : ''}`} aria-label={text}>
      {words.map((word, wordIndex) => (
        <span key={`${word}-${wordIndex}`} style={{ display: 'contents' }}>
          <span className="split-word">
            {[...word].map((char) => {
              const currentIndex = charIndex
              charIndex += 1

              return (
                <span
                  aria-hidden="true"
                  className="split-char"
                  key={`${char}-${currentIndex}`}
                  style={{ '--char-index': currentIndex }}
                >
                  {char}
                </span>
              )
            })}
          </span>
          {(wordIndex + 1) % 2 === 0 && wordIndex !== words.length - 1 && (
            <div key={`br-${wordIndex}`} style={{ width: '100%', height: 0 }} />
          )}
        </span>
      ))}
    </h1>
  )
}

export default SplitHeadline
