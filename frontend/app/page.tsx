"use client";
import { useEffect, useState } from "react";

type RaceResult = {
  race: string;
  top3: string[];
};

export default function Home() {
  const [results, setResults] = useState<RaceResult[]>([]);
  const [year, setYear] = useState("2024");

  useEffect(() => {
    // Render上のバックエンドURLに変更
    fetch(`https://f1-results-app.onrender.com/results/${year}`)
      .then((res) => res.json())
      .then((data) => setResults(data))
      .catch((err) => console.error("API fetch failed:", err));
  }, [year]);

  return (
    <main style={{ padding: "20px" }}>
      <h1>F1 Results {year}</h1>
      <select value={year} onChange={(e) => setYear(e.target.value)}>
        <option value="2024">2024</option>
        <option value="2023">2023</option>
        <option value="2022">2022</option>
      </select>
      <table border={1} cellPadding={6} style={{ marginTop: "20px" }}>
        <thead>
          <tr>
            <th>Race</th>
            <th>Top 3</th>
          </tr>
        </thead>
        <tbody>
          {results.map((r, i) => (
            <tr key={i}>
              <td>{r.race}</td>
              <td>{r.top3.join(", ")}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
