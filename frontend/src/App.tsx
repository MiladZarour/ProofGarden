import { Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import InvestigationDetail from "./pages/InvestigationDetail";
import NewInvestigation from "./pages/NewInvestigation";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/new" element={<NewInvestigation />} />
        <Route path="/investigations/:id" element={<InvestigationDetail />} />
      </Routes>
    </Layout>
  );
}

