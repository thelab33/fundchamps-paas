export default function SiteFooter() {
  return (
    <footer className="border-t border-brand/10 bg-ivory py-10 text-sm">
      <div className="container mx-auto flex flex-col items-center gap-2 px-4 text-brand/70">
        <p>&copy; {new Date().getFullYear()} LuxeFund. All rights reserved.</p>
        <p className="flex gap-4">
          <a href="/privacy" className="hover:text-gold">
            Privacy
          </a>
          <a href="/terms" className="hover:text-gold">
            Terms
          </a>
          <a href="mailto:support@luxefund.app" className="hover:text-gold">
            Contact
          </a>
        </p>
      </div>
    </footer>
  );
}
