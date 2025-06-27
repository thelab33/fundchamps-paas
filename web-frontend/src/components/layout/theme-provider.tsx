'use client';
import { ThemeProvider as NextThemeProvider } from 'next-themes';
import { ReactNode } from 'react';

export function ThemeProvider({
  children,
  attribute = 'class',
  defaultTheme = 'system',
}: {
  children: ReactNode;
  attribute?: string;
  defaultTheme?: string;
}) {
  return (
    <NextThemeProvider attribute={attribute} defaultTheme={defaultTheme} enableSystem>
      {children}
    </NextThemeProvider>
  );
}
