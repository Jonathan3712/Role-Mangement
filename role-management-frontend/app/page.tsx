"use client";

import React, { useEffect, useState } from "react";

type Role = {
  id: number;
  username: string;
  role: string;
};

export default function HomePage() {
  const [roles, setRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/roles")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`API error: ${res.status}`);
        }
        return res.json();
      })
      .then((data: Role[]) => {
        setRoles(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("Failed to load roles from backend");
        setLoading(false);
      });
  }, []);

  return (
    <main
      style={{
        minHeight: "100vh",
        padding: "2rem 4rem",
        backgroundColor: "#0f172a",
        color: "#f9fafb",
        fontFamily:
          'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
      }}
    >
      <header style={{ maxWidth: 720, marginBottom: "2rem" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "0.5rem" }}>
          Role Management Portal
        </h1>
        <p style={{ color: "#cbd5f5" }}>
          View and manage roles across Software Engineering, HR, and Payroll.
        </p>
      </header>

      {loading && <p>Loading roles...</p>}
      {error && <p style={{ color: "#f97373" }}>{error}</p>}

      {!loading && !error && (
        <section
          style={{
            display: "grid",
            gap: "1.5rem",
            gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
          }}
        >
          {roles.map((r) => (
            <article
              key={r.id}
              style={{
                backgroundColor: "#111827",
                borderRadius: "0.75rem",
                padding: "1.5rem",
                boxShadow: "0 10px 25px rgba(0,0,0,0.3)",
                border: "1px solid #1f2937",
              }}
            >
              <h2
                style={{
                  fontSize: "1.3rem",
                  marginBottom: "0.25rem",
                }}
              >
                {r.username}
              </h2>
              <p style={{ color: "#9ca3af" }}>Role: {r.role}</p>
            </article>
          ))}
        </section>
      )}
    </main>
  );
}
