"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/api";

export function CreateAppForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const form = new FormData(e.currentTarget);
    try {
      const app = await api.createApplication({
        name: form.get("name") as string,
        display_name: form.get("display_name") as string,
        team: form.get("team") as string,
        description: (form.get("description") as string) || undefined,
      });
      router.push(`/applications/${app.id}`);
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create");
    } finally {
      setLoading(false);
    }
  }

  const inputStyle = {
    width: "100%",
    padding: "0.5rem",
    background: "#1e293b",
    border: "1px solid #334155",
    borderRadius: 6,
    color: "#e2e8f0",
    marginTop: 4,
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        background: "#1e293b",
        padding: "1.25rem",
        borderRadius: 8,
        marginTop: "1rem",
        display: "grid",
        gap: "0.75rem",
      }}
    >
      <h3 style={{ margin: 0 }}>Create Application</h3>

      <label>
        App name (slug)
        <input name="name" required pattern="[a-z][a-z0-9-]*" placeholder="payment-api" style={inputStyle} />
      </label>
      <label>
        Display name
        <input name="display_name" required placeholder="Payment API" style={inputStyle} />
      </label>
      <label>
        Team
        <input name="team" required pattern="[a-z][a-z0-9-]*" placeholder="platform" style={inputStyle} />
      </label>
      <label>
        Description
        <input name="description" placeholder="Optional" style={inputStyle} />
      </label>

      {error && <p style={{ color: "#f87171", margin: 0 }}>{error}</p>}

      <button
        type="submit"
        disabled={loading}
        style={{
          padding: "0.6rem 1rem",
          background: "#2563eb",
          color: "white",
          border: "none",
          borderRadius: 6,
          cursor: loading ? "wait" : "pointer",
        }}
      >
        {loading ? "Creating…" : "Create Application"}
      </button>
    </form>
  );
}
