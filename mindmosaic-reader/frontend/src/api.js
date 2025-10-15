export async function analyzeMedicalText(text, userContext = null) {
  const requestBody = { text };
  if (userContext) {
    requestBody.user_context = userContext;
  }
  
  const res = await fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(requestBody),
  });
  
  if (!res.ok) {
    throw new Error(`API request failed: ${res.status} ${res.statusText}`);
  }
  
  return await res.json();
}

export async function getUserProfile() {
  const res = await fetch("http://127.0.0.1:8000/profile", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  return await res.json();
}
