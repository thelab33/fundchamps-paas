// Hero overlay quote that floats near the bottom-center of the hero
export default function HeroOverlayQuote() {
  return (
    <figure
      id="hero-overlay-quote"
      className="absolute bottom-28 left-1/2 z-10 w-[90%] max-w-3xl -translate-x-1/2 text-center md:bottom-32"
      aria-label="Motivational Quote"
    >
      <blockquote
        cite="https://connectatxelite.com/coach"
        className="animate-fade-in delay-700 text-sm font-medium italic text-white opacity-90 drop-shadow-lg sm:text-base"
        aria-live="polite"
      >
        <span
          className="block leading-relaxed"
          style={{ textShadow: '0 2px 12px rgba(0,0,0,.32)' }}
        >
          “The brotherhood and discipline we build here creates leaders for life.”
        </span>
      </blockquote>
      <figcaption className="mt-2 font-semibold not-italic text-yellow-200">
        — Coach&nbsp;A.&nbsp;Rodriguez
      </figcaption>
    </figure>
  );
}
