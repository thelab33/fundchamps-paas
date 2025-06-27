type Testimonial = { id: number; quote: string; author: string };

export default function Testimonials({ items }: { items: Testimonial[] }) {
  return (
    <section
      id="testimonials"
      className="bg-gradient-to-br from-black via-zinc-900 to-black/90 py-16"
    >
      <div className="container mx-auto max-w-3xl px-4 text-center">
        <h2 className="heading-gradient mb-8 flex items-center justify-center gap-2 text-4xl font-black md:text-5xl">
          💬 Testimonials
        </h2>

        <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
          {items.map((t, i) => (
            <blockquote
              key={t.id}
              className="animate-fade-in rounded-2xl bg-zinc-800/60 p-6 text-left shadow"
              style={{ animationDelay: `${i * 0.1}s` }}
            >
              <p className="text-lg italic text-yellow-100">“{t.quote}”</p>
              <footer className="mt-4 font-bold text-yellow-300">— {t.author}</footer>
            </blockquote>
          ))}
        </div>

        <p className="mt-10 text-zinc-300">
          Want to leave your feedback?{' '}
          <a
            href="#contact"
            className="underline transition hover:text-yellow-300 text-yellow-400"
          >
            Contact us
          </a>
        </p>
      </div>
    </section>
  );
}
