'use client';
import Link from 'next/link';

export default function SiteHeader() {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-brand/10 bg-ivory/80 backdrop-blur">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link href="/" className="text-lg font-semibold">
          LuxeFund
        </Link>
        <nav className="flex gap-6 text-sm">
          <Link href="/pricing" className="hover:text-gold">
            Pricing
          </Link>
          <Link href="/login" className="rounded-luxe bg-gold px-4 py-1.5 text-brand hover:bg-gold/90">
            Launch my team
          </Link>
        </nav>
      </div>
    </header>
  );
}
