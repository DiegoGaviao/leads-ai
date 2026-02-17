import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LandingPage } from './components/LandingPage';
import { Dashboard } from './components/Dashboard';

// Novas Páginas do Flow Automatizado
import OnboardingPage from './pages/OnboardingPage';
import ConnectInstagramPage from './pages/ConnectInstagram';
import CallbackPage from './pages/CallbackPage';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background text-foreground selection:bg-primary/30">

        <Routes>
          {/* Landing Page (Venda) */}
          <Route path="/" element={<LandingPage />} />

          {/* Flow de Onboarding (Pós-Venda) */}
          <Route path="/setup" element={<OnboardingPage />} />
          <Route path="/connect" element={<ConnectInstagramPage />} />
          <Route path="/callback" element={<CallbackPage />} />

          {/* Dashboard (Uso Diário) */}
          <Route path="/dashboard" element={<Dashboard />} />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>

        {/* Global FX */}
        <div className="fixed top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/10 blur-[120px] rounded-full -z-10 pointer-events-none" />
        <div className="fixed bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-secondary/10 blur-[120px] rounded-full -z-10 pointer-events-none" />
      </div>
    </BrowserRouter>
  );
}

export default App;
