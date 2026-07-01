const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://api.platform.ocp1.npd.co";

export type Application = {
  id: string;
  name: string;
  display_name: string;
  team: string;
  template: string;
  status: string;
  namespace: string;
  description: string | null;
  created_at: string;
  updated_at: string;
};

export type ApplicationList = {
  items: Application[];
  total: number;
};

export type Artifacts = {
  application_id: string;
  artifacts: Record<string, string>;
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    cache: "no-store",
  });

  if (!res.ok) {
    const body = await res.text();
    throw new Error(body || res.statusText);
  }

  return res.json();
}

export const api = {
  listApplications: () => request<ApplicationList>("/api/v1/applications"),

  getApplication: (id: string) => request<Application>(`/api/v1/applications/${id}`),

  createApplication: (data: {
    name: string;
    display_name: string;
    team: string;
    description?: string;
  }) =>
    request<Application>("/api/v1/applications", {
      method: "POST",
      body: JSON.stringify({ ...data, template: "web-api" }),
    }),

  provisionApplication: (id: string) =>
    request(`/api/v1/applications/${id}/provision`, { method: "POST" }),

  getArtifacts: (id: string) => request<Artifacts>(`/api/v1/applications/${id}/artifacts`),
};
