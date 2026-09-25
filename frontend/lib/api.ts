const API_BASE_URL = "https://hospitality-backend-ojog.onrender.com";

export async function refreshAccessToken(refreshToken: string) {
  const res = await fetch(`${API_BASE_URL}/api/token/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: refreshToken }),
  });
  if (!res.ok) throw new Error("Session expired");
  return res.json(); // { access }
}

export async function loginRequest(username: string, password: string) {
  const res = await fetch(`${API_BASE_URL}/api/token/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) {
    throw new Error("Invalid username or password");
  }

  return res.json(); // { access, refresh }
}

export async function authenticatedFetch(path: string, token: string) {
  let res = await fetch(`${API_BASE_URL}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (res.status === 401) {
    const refreshToken = sessionStorage.getItem("refresh_token");
    if (!refreshToken) throw new Error("Not authenticated");

    const { access } = await refreshAccessToken(refreshToken);
    sessionStorage.setItem("access_token", access);

    res = await fetch(`${API_BASE_URL}${path}`, {
      headers: { Authorization: `Bearer ${access}` },
    });
  }

  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }

  return res.json();
}

export async function registerRequest(data: {
  username: string;
  email: string;
  password: string;
  role: string;
  phone_number: string;
}) {
  const res = await fetch(`${API_BASE_URL}/api/users/register/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => null);
    throw new Error(errorData?.username?.[0] || errorData?.email?.[0] || "Registration failed");
  }

  return res.json();
}