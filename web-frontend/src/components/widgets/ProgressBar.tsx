// src/components/widgets/ProgressBar.tsx
type Props = { value: number; goal: number };

export default function ProgressBar({ value, goal }: Props) {
  const pct = Math.min(100, Math.round((value / goal) * 100));
  return (
    <div className="w-full rounded-luxe bg-brand/10">
      <div
        className="rounded-luxe bg-gold py-1 text-center text-xs font-medium text-brand transition-[width]"
        style={{ width: `${pct}%` }}
      >
        {pct}%
      </div>
    </div>
  );
}
