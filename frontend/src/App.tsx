import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Header from './components/Header'
import Home from './pages/Home'
import JobsPage from './pages/JobsPage'
import Login from './pages/Login'
import Register from './pages/Register'
import TechTrendsPage from './pages/TechTrendsPage'
import { AuthProvider } from './contexts/AuthProvider'

// Créer une instance de QueryClient pour react-query
const queryClient = new QueryClient()

/**
 * Main App component for JobTech Radar
 * Serves as the root component for the application
 */
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <div className="min-h-screen bg-gray-50 flex flex-col">
            <Header />
            <main className="flex-grow">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/jobs" element={<JobsPage />} />
                <Route path="/tech-trends" element={<TechTrendsPage />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
              </Routes>
            </main>
          </div>
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App
