'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import ProgressBar from '@/components/widgets/ProgressBar';
import HeroOverlayQuote from '@/components/widgets/HeroOverlayQuote';

type HeroProps = {
  /** dollars raised so far */
  raised: number;
  /** campaign goal in dollars */
  goal: number;
  /** optional first name for the greeting */
  currentUserName?: string;
};

export default function Hero({ raised = 18500, goal = 25000, currentUserName }: HeroProps) {
  const badges = [
    '🏅 Trusted by 500+ Families',
    '📚 Top 1% Academic Athletes',
    '🏀 AAU Gold Certified',
  ];

  return (
    <section
      id="hero-main"
      className="connect-hero relative flex min-h-[92vh] flex-col items-center justify-center overflow-hidden md:min-h-screen"
      aria-labelledby="hero-heading"
      tabIndex={-1}
    >
      {/* 🔥 Ken-Burns background */}
      <div className="pointer-events-none absolute inset-0 -z-10 overflow-hidden">
        <img
          src="/images/connect-atx-team.jpg"
          alt="Team huddle during pre-game"
          className="h-full w-full scale-110 object-cover opacity-95 animate-kenburns"
          loading="eager"
          decoding="async"
        />
        <div className="absolute inset-0 bg-[var(--overlay-glass)] backdrop-blur-sm" />
        {/* Decorative gradient stripes */}
        <div className="pointer-events-none absolute left-0 top-0 z-0 flex h-24 w-full select-none gap-3 opacity-60">
          <div className="flex-1 rounded-r-full blur-xl bg-gradient-to-r from-red-600 via-gold/80 to-white" />
          <div className="flex-1 rounded-l-full blur-xl bg-gradient-to-l from-gold via-black to-red-600" />
        </div>
      </div>

      {/* 🔥 Hero Content */}
      <div
        className="container relative z-20 mx-auto flex max-w-3xl flex-col items-center px-4 py-20 text-center"
        data-aos="fade-up"
      >
        {/* Logo */}
        <picture>
          <source srcSet="/images/logo.webp" type="image/webp" />
          <img
            src="/images/logo.png"
            alt="Connect ATX Elite logo"
            className="mb-6 h-32 w-32 rounded-full border-4 border-yellow-300 bg-white/80 shadow-xl animate-fade-in"
            loading="lazy"
            decoding="async"
          />
        </picture>

        {/* Personal greeting (optional) */}
        {currentUserName && (
          <div className="mb-5 inline-flex animate-shine items-center gap-2 rounded-xl bg-gradient-to-r from-yellow-400 to-yellow-200 px-6 py-2 font-semibold text-zinc-900 shadow">
            Welcome,&nbsp;{currentUserName}
            <span className="ml-1 animate-sparkle">✨</span>
          </div>
        )}

        {/* Headline */}
        <motion.h1
          id="hero-heading"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="animate-slide-up text-5xl font-extrabold tracking-tight text-white drop-shadow-xl sm:text-6xl"
        >
          Connect ATX Elite
        </motion.h1>

        {/* Sub-headline */}
        <p className="animate-slide-up delay-100 mt-4 max-w-xl text-lg text-zinc-100/90 sm:text-xl">
          Empowering Youth Through Basketball, Brotherhood&nbsp;&amp;&nbsp;Academics
        </p>

        {/* CTA */}
        <Link
          href="#tiers"
          className="animate-pop delay-200 mt-6 inline-block rounded-full bg-yellow-400 px-8 py-3 font-bold text-zinc-900 shadow-lg transition hover:bg-yellow-300"
          style={{ boxShadow: '0 4px 24px rgba(250,204,21,.18)' }}
        >
          Become a Sponsor
        </Link>

        {/* Impact badges */}
        <div
          className="animate-fade-in delay-500 mt-8 flex flex-wrap justify-center gap-4"
          aria-label="Program Impact Highlights"
        >
          {badges.map((b) => (
            <span key={b} className="badge-glass">
              {b}
            </span>
          ))}
        </div>
      </div>

      {/* 💰 Fundraising HUD */}
      <div className="relative z-30 mt-12 w-full max-w-xl px-4 animate-fade-in delay-300">
        <ProgressBar value={raised} goal={goal} />
        <p className="mt-3 text-center text-sm font-semibold text-white">
          💰{' '}
          <span className="font-bold text-yellow-300">${raised.toLocaleString()}</span> raised of{' '}
          <span className="font-bold text-yellow-300">${goal.toLocaleString()}</span>
        </p>
      </div>

      {/* ⬇ Scroll hint */}
      <button
        id="scroll-hint-hero"
        aria-label="Scroll down to explore"
        className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce focus:outline-none"
      >
        <svg
          className="h-8 w-8 text-yellow-400 drop-shadow"
          fill="none"
          stroke="currentColor"
          strokeWidth={2}
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* 💬 Motivational Quote Overlay */}
      <HeroOverlayQuote />
    </section>
  );
}
