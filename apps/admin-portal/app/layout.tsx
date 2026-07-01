export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "system-ui, sans-serif", background: "#0f172a", color: "#e2e8f0" }}>
        <header style={{ borderBottom: "1px solid #334155", padding: "1rem 2rem" }}>
          <h1 style={{ margin: 0, fontSize: "1.25rem" }}>
            <a href="/" style={{ color: "#38bdf8", textDecoration: "none" }}>
              Phoenix Platform
            </a>
          </h1>
        </header>
        <main style={{ maxWidth: 960, margin: "0 auto", padding: "2rem" }}>{children}</main>
      </body>
    </html>
  );
}
