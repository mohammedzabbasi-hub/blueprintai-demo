import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import AppLayout from "./components/AppLayout";
import Landing from "./pages/Landing";
import Index from "./pages/Index";
import CreativeLibrary from "./pages/CreativeLibrary";
import CreativeDetail from "./pages/CreativeDetail";
import VideoAnalysis from "./pages/VideoAnalysis";
import AdBriefs from "./pages/AdBriefs";
import Recommendations from "./pages/Recommendations";
import Settings from "./pages/Settings";
import ActivityLog from "./pages/ActivityLog";
import ConnectShop from "./pages/ConnectShop";
import Login from "./pages/Login";
import Onboarding from "./pages/Onboarding";
import Creators from "./pages/Creators";
import CreatorDetail from "./pages/CreatorDetail";
import NotFound from "./pages/NotFound";
import RevenueBlueprint from "./pages/RevenueBlueprint";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/onboarding" element={<Onboarding />} />

        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<Index />} />
          <Route path="/creative-library" element={<CreativeLibrary />} />
          <Route path="/creatives/:id" element={<CreativeDetail />} />
          <Route path="/upload" element={<VideoAnalysis />} />
          <Route path="/ad-briefs" element={<AdBriefs />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/revenue-blueprint" element={<RevenueBlueprint />} />
          <Route path="/creators" element={<Creators />} />
          <Route path="/creators/:creatorId" element={<CreatorDetail />} />
          <Route path="/connect-shop" element={<ConnectShop />} />
          <Route path="/connect" element={<ConnectShop />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/activity-log" element={<ActivityLog />} />
        </Route>

        <Route path="/home" element={<Navigate to="/" replace />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}