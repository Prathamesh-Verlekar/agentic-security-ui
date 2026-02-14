import { BrowserRouter, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import AdminDashboard from "./pages/AdminDashboard";
import AdminLogin from "./pages/AdminLogin";
import ArticleView from "./pages/ArticleView";
import ItemDetailPage from "./pages/ItemDetailPage";
import ItemList from "./pages/ItemList";
import Landing from "./pages/Landing";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main className="main-content">
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<Landing />} />
          <Route path="/:category" element={<ItemList />} />
          <Route path="/:category/:id" element={<ItemDetailPage />} />

          {/* Hidden admin routes — no public links point here */}
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/admin/articles/:id" element={<ArticleView />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
