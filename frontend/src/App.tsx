import Header from './components/Header'
import Home from './pages/Home'

/**
 * Main App component for JobTech Radar
 * Serves as the root component for the application
 */
function App() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />
      <Home />
    </div>
  )
}

export default App
