// src/app/page.tsx
import { Hero } from '@/components/sections';           // <- barrel export keeps imports tidy
import { SponsorWall, Testimonials, Leaderboard } from '@/components/sections';
import FundraiserMeter from '@/components/widgets/FundraiserMeter';

// ----- TEMP mocked data – swap for Flask API fetches later -----
const sponsors = [
  { id: 1, name: 'GoldStar Bank', amount: 5000, logoUrl: '/sponsors/goldstar.svg' },
  { id: 2, name: 'Elite Sports Co.', amount: 3500, logoUrl: '/sponsors/elite.svg' },
  { id: 3, name: 'Royal Motors', amount: 2500, logoUrl: '/sponsors/royal.svg' },
];

const testimonials = [
  {
    id: 1,
    quote:
      'Connect ATX Elite changed my son’s life. He found a brotherhood and his grades improved too!',
    author: 'Parent, Class of 2024',
  },
  {
    id: 2,
    quote: 'The coaches care about more than basketball. They help us become leaders.',
    author: 'Team Captain',
  },
];
// ---------------------------------------------------------------

export default function Home() {
  const goal = 25_000;
  const raised = 18_500;

  return (
    <>
      {/* Luxe hero with built-in progress HUD */}
      <Hero raised={raised} goal={goal} currentUserName="Alex" />

      {/* Stand-alone fundraising meter (optional extra) */}
      <section className="container mx-auto max-w-2xl px-4 py-12">
        <h2 className="mb-4 text-center text-2xl font-semibold">Campaign Progress</h2>
        <FundraiserMeter raised={raised} goal={goal} />
      </section>

      {/* VIP sponsor leaderboard (compact grid) */}
      <Leaderboard sponsors={sponsors} />

      {/* Full sponsor wall with modal CTA */}
      <SponsorWall sponsors={sponsors} />

      {/* Social proof testimonials */}
      <Testimonials items={testimonials} />
    </>
  );
}

