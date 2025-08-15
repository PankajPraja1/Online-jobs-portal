import React, { useState } from "react";
import api from "../services/api";
import { setAuthToken } from "../services/api";
export default function UploadResume(){
  const [file, setFile] = useState(null);
  const [matches, setMatches] = useState([]);

  const submit = async e => {
    e.preventDefault();
    const fd = new FormData();
    fd.append("resume", file);
    const res = await api.post("resume/match/", fd, { headers: { 'Content-Type': 'multipart/form-data' }});
    setMatches(res.data.matches);
  };

  return (
    <div>
      <h2>Upload Resume & Find Matches</h2>
      <form onSubmit={submit}>
        <input type="file" onChange={e=>setFile(e.target.files[0])} />
        <button>Upload & Match</button>
      </form>
      <h3>Matches</h3>
      <ul>
        {matches.map(m => (
          <li key={m.job_id}>
            {m.title} — score: {m.score.toFixed(3)}
          </li>
        ))}
      </ul>
    </div>
  );
}
