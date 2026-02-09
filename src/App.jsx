import { useState } from 'react'
import './App.css'
import URLsTable from './URLsTable'

function App() {
  const [jobDescription, setJobDescription] = useState('')
  const [role, setRole] = useState('Software Engineer')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [view, setView] = useState('form') // 'form' or 'table'

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')
    
    try {
      // Send POST request to FastAPI backend
      const response = await fetch('http://localhost:8000/api/submit-job-description', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ job_description: jobDescription, role })
      })
      
      // Check if request was successful
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      // Parse the JSON response
      const data = await response.json()
      
      console.log('Response from backend:', data)
      setMessage(`✓ ${data.message}`)
      setJobDescription('') // Clear the input field
      
    } catch (error) {
      console.error('Error submitting URL:', error)
      setMessage(`✗ Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <nav className="nav-tabs">
        <button 
          className={`nav-tab ${view === 'form' ? 'active' : ''}`}
          onClick={() => setView('form')}
        >
          Submit Job Description
        </button>
        <button 
          className={`nav-tab ${view === 'table' ? 'active' : ''}`}
          onClick={() => setView('table')}
        >
          View All Submissions
        </button>
      </nav>

      {view === 'form' ? (
        <div className="form-container">
          <h1>Job Description Submission</h1>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Select Role:</label>
              <div className="radio-group">
                <label className="radio-label">
                  <input
                    type="radio"
                    name="role"
                    value="Software Engineer"
                    checked={role === 'Software Engineer'}
                    onChange={(e) => setRole(e.target.value)}
                    disabled={loading}
                  />
                  <span>Software Engineer</span>
                </label>
                <label className="radio-label">
                  <input
                    type="radio"
                    name="role"
                    value="AI/ML Developer"
                    checked={role === 'AI/ML Developer'}
                    onChange={(e) => setRole(e.target.value)}
                    disabled={loading}
                  />
                  <span>AI/ML Developer</span>
                </label>
                <label className="radio-label">
                  <input
                    type="radio"
                    name="role"
                    value="Salesforce Developer"
                    checked={role === 'Salesforce Developer'}
                    onChange={(e) => setRole(e.target.value)}
                    disabled={loading}
                  />
                  <span>Salesforce Developer</span>
                </label>
                <label className="radio-label">
                  <input
                    type="radio"
                    name="role"
                    value="Salesforce Administrator"
                    checked={role === 'Salesforce Administrator'}
                    onChange={(e) => setRole(e.target.value)}
                    disabled={loading}
                  />
                  <span>Salesforce Administrator</span>
                </label>
              </div>
            </div>
            <div className="form-group">
              <label htmlFor="job-desc-input">Enter Job Description (up to 10,000 characters):</label>
              <textarea
                id="job-desc-input"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
                required
                disabled={loading}
                rows={10}
                maxLength={10000}
              />
              <div className="char-count">
                {jobDescription.length} / 10,000 characters
              </div>
            </div>
            <button type="submit" disabled={loading}>
              {loading ? 'Submitting...' : 'Submit'}
            </button>
          </form>
          {message && (
            <div className={`message ${message.startsWith('✓') ? 'success' : 'error'}`}>
              {message}
            </div>
          )}
        </div>
      ) : (
        <URLsTable />
      )}
    </div>
  )
}

export default App
