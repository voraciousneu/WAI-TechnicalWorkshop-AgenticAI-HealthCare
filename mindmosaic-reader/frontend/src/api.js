export async function analyzeText(text, userSpeed = null) {
  const res = await fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, user_speed: userSpeed }),
  });
  return await res.json();
}
