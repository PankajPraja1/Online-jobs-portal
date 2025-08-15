import React, { useState, useEffect } from "react";
import api from "../services/api";
import { Link } from "react-router-dom";

export default function JobList(){
  const [jobs, setJobs] = useState([]);
  const [q,setQ] = useState("");

  useEffect(()=> { fetchJobs(); }, []);

  const fetchJobs = async () => {
    const res = await api.get("jobs/?q=" + encodeURIComponent(q));
    setJobs(res.data);
  };

  return (
    <div>
      <h2>Jobs</h2>
      <input value={q} onChange={e=>setQ(e.target.value)} placeholder="search" />
      <button onClick={fetchJobs}>Search</button>
      <ul>
        {jobs.map(j=>(
          <li key={j.id}>
            <Link to={"/jobs/"+j.id}>{j.title}</Link> — {j.employer.username} — {j.skills}
          </li>
        ))}
      </ul>
    </div>
  );
}
