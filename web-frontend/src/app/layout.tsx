// src/app/layout.tsx
import './globals.css';

import { ThemeProvider } from '@/components/layout/theme-provider';
import SiteHeader from '@/components/layout/SiteHeader';
import SiteFooter from '@/components/layout/SiteFooter';

import { Geist, Geist_Mono } from 'next/font/google';
import { Metadata } from 'next';
import { ScrollRestoration } from 'next/dist/client/components/scroll-restoration';

const geist = Geist({ subsets: ['latin'], variable: '--font-sans' });
const mono  = Geist_Mono({ subsets: ['latin'], variable: '--font-mono' });

export const metadata: Metadata = {
  title: 'Luxury Digital Fundraising',
  description: 'Elite youth & nonprofit fundraising made effortless.',
  authors: [{ name: 'LuxeFund', url: 'https://luxefund.app' }],
  metadataBase: new URL('https://luxefund.app'),
  openGraph: {
    title: 'Luxury Digital Fundraising',
    description:
      'Launch a white-glove fundraising campaign in minutes. Delight every donor.',
    images: '/og-image.png',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    creator: '@luxefund',
    images: '/og-image.png',
  },
  // iOS dark/light auto-theme hint
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#F8F7F4' },
    { media: '(prefers-color-scheme: dark)', color: '#0D0D0D' },
  ],
  // extra security / perf headers
  referrer: 'strict-origin-when-cross-origin',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${geist.variable} ${mono.variable}`}
    >
      <head>
        {/* Progressive Web App bits */}
        <meta name="viewport" content="width=device-width,initial-scale=1" />
        <link rel="manifest" href="/manifest.json" crossOrigin="use-credentials" />
        {/* DNS-prefetch for Stripe CDN & images */}
        <meta httpEquiv="x-dns-prefetch-control" content="on" />
        <link rel="dns-prefetch" href="//js.stripe.com" />
        <link rel="preconnect" href="https://cdn.luxefund.app" crossOrigin="" />
        {/* Favicon */}
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
      </head>

      <body
        className="bg-ivory text-brand selection:bg-gold/30 motion-safe:transition-colors"
        // page-transition classes (optional, works with Framer Motion)
        data-theme-transition
      >
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          <SiteHeader />
          <main className="min-h-[calc(100vh-8rem)]">{children}</main>
          <SiteFooter />
        </ThemeProvider>

        {/* Restore scroll position on back/forward nav */}
        <ScrollRestoration />
      </body>
    </html>
  );
}

