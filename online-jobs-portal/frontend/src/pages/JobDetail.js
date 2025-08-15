import React, { useState, useEffect } from "react";
import api from "../services/api";
import { useParams } from "react-router-dom";

export default function JobDetail(){
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [resume, setResume] = useState(null);
  const [cover, setCover] = useState("");

  useEffect(()=>{
    api.get(`jobs/${id}/`).then(r=>setJob(r.data));
  }, [id]);

  const apply = async e => {
    e.preventDefault();
    const form = new FormData();
    form.append("resume", resume);
    form.append("cover_letter", cover);
    await api.post(`jobs/${id}/apply/`, form, { headers: { 'Content-Type': 'multipart/form-data' }});
    alert("Applied");
  };

  if(!job) return <div>Loading...</div>;
  return (
    <div>
      <h2>{job.title}</h2>
      <p>{job.description}</p>
      <p><strong>Skills:</strong> {job.skills}</p>

      <h3>Apply</h3>
      <form onSubmit={apply}>
        <input type="file" onChange={e=>setResume(e.target.files[0])} required />
        <textarea placeholder="Cover letter" value={cover} onChange={e=>setCover(e.target.value)} />
        <button>Apply</button>
      </form>
    </div>
  );
}
