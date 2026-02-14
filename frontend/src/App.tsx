import { BrowserRouter, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import AdminDashboard from "./pages/AdminDashboard";
import AdminLogin from "./pages/AdminLogin";
import ArticleView from "./pages/ArticleView";
import CareerDetailPage from "./pages/CareerDetailPage";
import CareerLanding from "./pages/CareerLanding";
import CareerTransitionsPage from "./pages/CareerTransitionsPage";
import ItemDetailPage from "./pages/ItemDetailPage";
import ItemList from "./pages/ItemList";
import Landing from "./pages/Landing";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main className="main-content">
        <Routes>
          {/* Landing */}
          <Route path="/" element={<Landing />} />

          {/* Agentic Security routes */}
          <Route path="/guardrails" element={<ItemList />} />
          <Route path="/guardrails/:id" element={<ItemDetailPage />} />
          <Route path="/evals" element={<ItemList />} />
          <Route path="/evals/:id" element={<ItemDetailPage />} />

          {/* Career Counselor routes */}
          <Route path="/careers" element={<CareerLanding />} />
          <Route path="/careers/transitions" element={<CareerTransitionsPage />} />
          <Route path="/careers/:id" element={<CareerDetailPage />} />

          {/* Hidden admin routes — no public links point here */}
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/admin/articles/:id" element={<ArticleView />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
