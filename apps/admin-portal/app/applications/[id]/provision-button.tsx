"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/api";

export function ProvisionButton({ appId }: { appId: string }) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleProvision() {
    setLoading(true);
    setError(null);
    try {
      await api.provisionApplication(appId);
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Provision failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <button
        onClick={handleProvision}
        disabled={loading}
        style={{
          padding: "0.6rem 1.25rem",
          background: "#16a34a",
          color: "white",
          border: "none",
          borderRadius: 6,
          cursor: loading ? "wait" : "pointer",
          fontSize: "1rem",
        }}
      >
        {loading ? "Provisioning…" : "Run Golden Path"}
      </button>
      {error && <p style={{ color: "#f87171" }}>{error}</p>}
    </div>
  );
}
