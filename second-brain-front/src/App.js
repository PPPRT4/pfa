import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Notes from "./pages/Notes";

const isAuth = () => Boolean(sessionStorage.getItem("sb_user"));

const Private = ({ children }) =>
  isAuth() ? children : <Navigate to="/" replace />;

const Public = ({ children }) =>
  isAuth() ? <Navigate to="/notes" replace /> : children;

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/"      element={<Public><Login /></Public>} />
        <Route path="/notes" element={<Private><Notes /></Private>} />
        <Route path="*"      element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
