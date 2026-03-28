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
        <span className="split-word" key={`${word}-${wordIndex}`}>
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
      ))}
    </h1>
  )
}

export default SplitHeadline
