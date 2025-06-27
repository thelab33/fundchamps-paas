import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Trophy } from 'lucide-react';

type Sponsor = { id: number; name: string; amount: number; logoUrl: string };

export default function Leaderboard({ sponsors }: { sponsors: Sponsor[] }) {
  return (
    <section className="container mx-auto py-14">
      <h2 className="mb-8 flex items-center gap-2 text-3xl font-semibold">
        <Trophy className="size-6 text-gold" />
        VIP Sponsors
      </h2>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {sponsors.map((s) => (
          <Card
            key={s.id}
            className="bg-ivory/60 shadow-lg backdrop-blur-lg transition-shadow hover:shadow-gold/40"
          >
            <CardHeader className="flex items-center justify-between">
              <span className="font-medium">{s.name}</span>
              <span className="rounded-full bg-gold/20 px-3 py-1 text-xs text-gold">
                ${s.amount.toLocaleString()}
              </span>
            </CardHeader>
            <CardContent className="flex items-center justify-center py-6">
              <img
                src={s.logoUrl}
                alt={s.name}
                className="h-16 w-auto object-contain grayscale hover:grayscale-0"
              />
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}
