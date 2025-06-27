type MeterProps = { raised: number; goal: number };

export default function FundraiserMeter({ raised, goal }: MeterProps) {
  const pct = Math.min(100, Math.round((raised / goal) * 100));
  const milestoneEmoji =
    pct >= 100 ? '🏆' : pct >= 75 ? '🔥' : pct >= 50 ? '🚀' : pct >= 25 ? '⚡️' : '💤';

  return (
    <div
      role="region"
      aria-label="Fundraising Progress"
      className="flex flex-col gap-3 rounded-xl bg-black/60 p-4 shadow-lg
      backdrop-blur sm:flex-row sm:items-center"
    >
      {/* progress bar */}
      <div className="relative w-full sm:flex-1">
        <div
          role="progressbar"
          aria-valuemin={0}
          aria-valuemax={goal}
          aria-valuenow={raised}
          className="h-4 w-full overflow-hidden rounded-full bg-zinc-800"
        >
          <div
            className="h-full rounded-full bg-gradient-to-r from-yellow-400 to-yellow-200
            transition-all duration-700 ease-out"
            style={{ width: `${pct}%` }}
            aria-label="Current fundraising progress"
          />
        </div>
        <div
          className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full
          bg-yellow-300 px-2 py-0.5 text-xs font-bold text-zinc-900 shadow-lg"
        >
          {pct}%
        </div>
      </div>

      {/* numeric label */}
      <div className="whitespace-nowrap text-center text-sm font-semibold text-yellow-300 sm:text-left">
        Raised: ${raised.toLocaleString()} / ${goal.toLocaleString()}{' '}
        <span className="ml-2 text-xl" aria-hidden>
          {milestoneEmoji}
        </span>
      </div>
    </div>
  );
}
