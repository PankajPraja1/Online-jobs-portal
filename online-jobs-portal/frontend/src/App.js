import React, { useEffect } from "react";
import { Routes, Route, Link } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import JobList from "./pages/JobList";
import JobDetail from "./pages/JobDetail";
import PostJob from "./pages/PostJob";
import Profile from "./pages/Profile";
import UploadResume from "./pages/UploadResume";
import Matches from "./pages/Matches";
import { setAuthToken } from "./services/api";

function App() {
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    setAuthToken(token);
  }, []);

  const logout = () => {
    localStorage.removeItem("access_token");
    setAuthToken(null);
    window.location.href = "/";
  };

  return (
    <div style={{ padding: 20 }}>
      <nav>
        <Link to="/">Jobs</Link> | <Link to="/post-job">Post Job</Link> | <Link to="/upload-resume">Upload Resume</Link> | <Link to="/matches">Matches</Link> | <Link to="/profile">Profile</Link> | <a onClick={logout}>Logout</a>
      </nav>
      <hr />
      <Routes>
        <Route path="/" element={<JobList/>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/register" element={<Register/>} />
        <Route path="/jobs/:id" element={<JobDetail/>} />
        <Route path="/post-job" element={<PostJob/>} />
        <Route path="/upload-resume" element={<UploadResume/>} />
        <Route path="/matches" element={<Matches/>} />
        <Route path="/profile" element={<Profile/>} />
      </Routes>
    </div>
  );
}

export default App;
