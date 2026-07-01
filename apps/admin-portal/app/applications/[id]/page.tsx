import Link from "next/link";
import { api } from "@/lib/api";
import { ProvisionButton } from "./provision-button";

export default async function ApplicationPage({ params }: { params: { id: string } }) {
  const app = await api.getApplication(params.id);

  let artifacts: Record<string, string> | null = null;
  if (app.status === "provisioned") {
    try {
      const result = await api.getArtifacts(params.id);
      artifacts = result.artifacts;
    } catch {
      artifacts = null;
    }
  }

  return (
    <div>
      <Link href="/" style={{ color: "#94a3b8", fontSize: "0.9rem" }}>
        ← Back
      </Link>

      <h2 style={{ marginBottom: 4 }}>{app.display_name}</h2>
      <p style={{ color: "#94a3b8", marginTop: 0 }}>
        <code>{app.name}</code> · team <code>{app.team}</code> ·{" "}
        <span style={{ color: app.status === "provisioned" ? "#4ade80" : "#fbbf24" }}>{app.status}</span>
      </p>

      <dl style={{ display: "grid", gridTemplateColumns: "140px 1fr", gap: "0.5rem", fontSize: "0.9rem" }}>
        <dt style={{ color: "#64748b" }}>Namespace</dt>
        <dd style={{ margin: 0, fontFamily: "monospace" }}>{app.namespace}</dd>
        <dt style={{ color: "#64748b" }}>Template</dt>
        <dd style={{ margin: 0 }}>{app.template}</dd>
        <dt style={{ color: "#64748b" }}>Route</dt>
        <dd style={{ margin: 0, fontFamily: "monospace" }}>
          {app.name}-{app.team}.apps.ocp1.npd.co
        </dd>
      </dl>

      {app.status !== "provisioned" && (
        <div style={{ marginTop: "1.5rem" }}>
          <ProvisionButton appId={app.id} />
        </div>
      )}

      {artifacts && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Generated Artifacts ({Object.keys(artifacts).length})</h3>
          {Object.entries(artifacts).map(([name, content]) => (
            <details key={name} style={{ marginBottom: "0.75rem", background: "#1e293b", borderRadius: 8 }}>
              <summary style={{ padding: "0.75rem", cursor: "pointer", fontFamily: "monospace" }}>{name}</summary>
              <pre
                style={{
                  margin: 0,
                  padding: "1rem",
                  overflow: "auto",
                  fontSize: "0.8rem",
                  borderTop: "1px solid #334155",
                }}
              >
                {content}
              </pre>
            </details>
          ))}
        </div>
      )}
    </div>
  );
}
