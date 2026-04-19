import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import Introduction from "./pages/Introduction.tsx";
import Index from "./pages/Index.tsx";
import Register from "./pages/Register.tsx";
import ForgotPassword from "./pages/ForgotPassword.tsx";
import Dashboard from "./pages/Dashboard.tsx";
import ProjectGuidance from "./pages/ProjectGuidance.tsx";
import ProjectDetails from "./pages/ProjectDetails.tsx";   // Feature 1
import SkillGap from "./pages/SkillGap.tsx";
import NotFound from "./pages/NotFound.tsx";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/"                element={<Introduction />} />
          <Route path="/login"           element={<Index />} />
          <Route path="/register"        element={<Register />} />
          <Route path="/dashboard"       element={<Dashboard />} />
          <Route path="/project-guidance"element={<ProjectGuidance />} />
          <Route path="/project-details" element={<ProjectDetails />} />   {/* Feature 1 */}
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/skill-gap"       element={<SkillGap />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*"                element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
