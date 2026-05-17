function getToken() {
  return (
    localStorage.getItem("token") ||
    localStorage.getItem("access_token") ||
    localStorage.getItem("authToken")
  );
}

export async function getSavedOnboarding() {
  const token = getToken();

  const res = await fetch("/onboarding/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    throw new Error("Failed to load onboarding");
  }

  return res.json();
}

export async function saveOnboarding(data) {
  const token = getToken();

  localStorage.setItem("blueprintai_onboarding", JSON.stringify(data));

  const res = await fetch("/onboarding/me", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    throw new Error("Failed to save onboarding");
  }

  return res.json();
}
