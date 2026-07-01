import Link from "next/link";
import { api } from "@/lib/api";
import { CreateAppForm } from "./create-form";

const statusColor: Record<string, string> = {
  pending: "#fbbf24",
  provisioning: "#38bdf8",
  provisioned: "#4ade80",
  failed: "#f87171",
};

export default async function HomePage() {
  let apps: Awaited<ReturnType<typeof api.listApplications>> | null = null;
  let error: string | null = null;

  try {
    apps = await api.listApplications();
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load applications";
  }

  return (
    <div>
      <h2 style={{ marginTop: 0 }}>Applications</h2>
      <p style={{ color: "#94a3b8" }}>Self-service Golden Path — create and provision apps on OpenShift.</p>

      <CreateAppForm />

      {error && (
        <p style={{ color: "#f87171", background: "#450a0a", padding: "0.75rem", borderRadius: 8 }}>
          API error: {error}. Is platform-api running on port 8000?
        </p>
      )}

      {apps && apps.total === 0 && (
        <p style={{ color: "#94a3b8" }}>No applications yet. Create one above.</p>
      )}

      {apps && apps.items.length > 0 && (
        <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "1.5rem" }}>
          <thead>
            <tr style={{ borderBottom: "1px solid #334155", textAlign: "left" }}>
              <th style={{ padding: "0.5rem" }}>Name</th>
              <th style={{ padding: "0.5rem" }}>Team</th>
              <th style={{ padding: "0.5rem" }}>Namespace</th>
              <th style={{ padding: "0.5rem" }}>Status</th>
              <th style={{ padding: "0.5rem" }}></th>
            </tr>
          </thead>
          <tbody>
            {apps.items.map((app) => (
              <tr key={app.id} style={{ borderBottom: "1px solid #1e293b" }}>
                <td style={{ padding: "0.5rem" }}>{app.display_name}</td>
                <td style={{ padding: "0.5rem" }}>{app.team}</td>
                <td style={{ padding: "0.5rem", fontFamily: "monospace", fontSize: "0.85rem" }}>
                  {app.namespace}
                </td>
                <td style={{ padding: "0.5rem", color: statusColor[app.status] || "#e2e8f0" }}>
                  {app.status}
                </td>
                <td style={{ padding: "0.5rem" }}>
                  <Link href={`/applications/${app.id}`} style={{ color: "#38bdf8" }}>
                    View →
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
