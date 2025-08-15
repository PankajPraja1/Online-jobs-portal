import React, { useState } from "react";
import api from "../services/api";

export default function PostJob(){
  const [form, setForm] = useState({title:"",description:"",skills:"",location:"",min_experience:0});
  const submit = async e => {
    e.preventDefault();
    await api.post("jobs/", form);
    alert("Job posted");
  };
  return (
    <form onSubmit={submit}>
      <h2>Post Job</h2>
      <input placeholder="Title" onChange={e=>setForm({...form,title:e.target.value})}/>
      <textarea placeholder="Description" onChange={e=>setForm({...form,description:e.target.value})}/>
      <input placeholder="Skills (comma separated)" onChange={e=>setForm({...form,skills:e.target.value})}/>
      <input placeholder="Location" onChange={e=>setForm({...form,location:e.target.value})}/>
      <input type="number" placeholder="Min Experience" onChange={e=>setForm({...form,min_experience:parseInt(e.target.value||0)})}/>
      <button>Post</button>
    </form>
  );
}
