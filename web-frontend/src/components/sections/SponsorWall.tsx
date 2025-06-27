'use client';

import { useState } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardContent } from '@/components/ui/card';

type Sponsor = { id: number; name: string; logoUrl: string; amount: number };

export default function SponsorWall({ sponsors }: { sponsors: Sponsor[] }) {
  const [open, setOpen] = useState(false);

  return (
    <section
      id="sponsor-wall"
      className="relative bg-gradient-to-b from-black via-secondary to-black/90 py-10 md:py-16"
    >
      <div className="container mx-auto flex max-w-3xl flex-col items-center px-4">
        <h2 className="mb-6 flex items-center gap-3 text-3xl font-black heading-gradient md:text-5xl">
          🏆 Sponsor Wall <span className="prestige-badge ml-2">2025</span>
        </h2>

        <p className="mb-8 max-w-xl text-center text-lg text-white/80">
          Fueling dreams—thanks to every sponsor who supports our youth on and off the court!
        </p>

        {/* grid of sponsor cards */}
        <div className="mb-8 grid w-full grid-cols-1 gap-6 sm:grid-cols-2">
          {sponsors.map((s) => (
            <Card
              key={s.id}
              className="flex items-center justify-center bg-black/40 p-4 shadow-lg backdrop-blur"
            >
              <CardHeader className="flex w-full items-center justify-between">
                <span className="font-medium text-white">{s.name}</span>
                <span className="rounded-full bg-gold/20 px-3 py-0.5 text-xs text-gold">
                  ${s.amount.toLocaleString()}
                </span>
              </CardHeader>
              <CardContent className="flex w-full items-center justify-center py-4">
                <img
                  src={s.logoUrl}
                  alt={s.name}
                  className="h-14 w-auto object-contain grayscale hover:grayscale-0"
                />
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Become-a-Sponsor modal trigger */}
        <Dialog.Root open={open} onOpenChange={setOpen}>
          <Dialog.Trigger asChild>
            <Button className="btn-glow btn-primary mt-2 px-8 py-3 text-xl shadow-inner-gold">
              Become a Sponsor
            </Button>
          </Dialog.Trigger>

          <Dialog.Portal>
            <Dialog.Overlay className="fixed inset-0 z-[1000] bg-black/60 backdrop-blur-sm" />
            <Dialog.Content
              className="fixed left-1/2 top-1/2 z-[1001] w-[90%] max-w-md -translate-x-1/2 -translate-y-1/2
              rounded-2xl bg-gradient-to-br from-gold via-black to-red-700 p-8 text-center shadow-elevated"
            >
              <Dialog.Close asChild>
                <button
                  className="absolute right-3 top-3 text-2xl text-gold transition hover:text-red-500"
                  aria-label="Close sponsor modal"
                >
                  <X />
                </button>
              </Dialog.Close>

              <h3 className="mb-2 text-2xl font-bold text-gold">Become a Sponsor</h3>
              <p className="mb-4 text-white/80">
                Leave your mark—help us reach the championship!
              </p>

              {/* fake form for now */}
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  alert('Thanks for your support!  🎉');
                  setOpen(false);
                }}
                className="space-y-3"
              >
                <input
                  type="text"
                  required
                  placeholder="Your Name / Company"
                  className="w-full rounded bg-black/60 px-4 py-2 text-white
                  placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-gold"
                />
                <input
                  type="number"
                  required
                  placeholder="Sponsorship Amount"
                  className="w-full rounded bg-black/60 px-4 py-2 text-white
                  placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-gold"
                />
                <Button type="submit" className="btn-glow btn-primary w-full">
                  Sponsor Now
                </Button>
              </form>
            </Dialog.Content>
          </Dialog.Portal>
        </Dialog.Root>
      </div>
    </section>
  );
}
