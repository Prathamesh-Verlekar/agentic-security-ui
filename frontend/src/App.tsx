import { BrowserRouter, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import ItemDetailPage from "./pages/ItemDetailPage";
import ItemList from "./pages/ItemList";
import Landing from "./pages/Landing";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/:category" element={<ItemList />} />
          <Route path="/:category/:id" element={<ItemDetailPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
