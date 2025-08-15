import React, { useState } from "react";
import api, { setAuthToken } from "../services/api";
import { useNavigate } from "react-router-dom";

export default function Login(){
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const nav = useNavigate();

  const submit = async e => {
    e.preventDefault();
    try {
      const resp = await api.post("auth/login/", { username, password });
      localStorage.setItem("access_token", resp.data.access);
      localStorage.setItem("refresh_token", resp.data.refresh);
      setAuthToken(resp.data.access);
      nav("/");
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <form onSubmit={submit}>
      <h2>Login</h2>
      <input placeholder="username" value={username} onChange={e=>setUsername(e.target.value)} />
      <input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      <button>Login</button>
    </form>
  );
}
