const API_KEY = import.meta.env.VITE_OPENWEATHER_API_KEY;

export async function fetchCurrentUV(lat, lon) {
  const url = `https://api.openweathermap.org/data/3.0/onecall?lat=${lat}&lon=${lon}&exclude=minutely,hourly,alerts&units=metric&appid=${API_KEY}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch UV data");
  }

  const data = await response.json();
  return data;
}
