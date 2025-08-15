import React, { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

export default function Register(){
  const [form, setForm] = useState({username:"",email:"",password:"",is_employer:false});
  const nav = useNavigate();

  const submit=async e=>{
    e.preventDefault();
    try {
      await api.post("auth/register/", form);
      alert("Registered. Login now.");
      nav("/login");
    } catch (err) {
      alert("Registration failed");
    }
  };

  return (
    <form onSubmit={submit}>
      <h2>Register</h2>
      <input placeholder="username" onChange={e=>setForm({...form,username:e.target.value})} />
      <input placeholder="email" onChange={e=>setForm({...form,email:e.target.value})} />
      <input placeholder="password" type="password" onChange={e=>setForm({...form,password:e.target.value})} />
      <label><input type="checkbox" onChange={e=>setForm({...form,is_employer:e.target.checked})}/> Register as Employer</label>
      <button>Register</button>
    </form>
  );
}
