const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:5000';

export async function getLeaderboard(teamSlug: string) {
  const res = await fetch(`${API}/api/teams/${teamSlug}/sponsors`);
  if (!res.ok) throw new Error('Failed to fetch leaderboard');
  return res.json() as Promise<{ id: number; name: string; amount: number; logoUrl: string }[]>;
}
