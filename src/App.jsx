import { useState } from 'react'
import './App.css'
import URLsTable from './URLsTable'

function App() {
  const [jobDescription, setJobDescription] = useState('')
  const [role, setRole] = useState('Software Engineer')
  const [view, setView] = useState('form') // 'form' or 'table'

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    const submittedJobDesc = jobDescription
    const submittedRole = role
    
    setJobDescription('')
    
    fetch('http://localhost:8000/api/submit-job-description', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ job_description: submittedJobDesc, role: submittedRole })
    })
    .then(response => response.json())
    .then(data => console.log('Submitted:', data))
    .catch(error => console.error('Error:', error))
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
                rows={10}
                maxLength={10000}
              />
              <div className="char-count">
                {jobDescription.length} / 10,000 characters
              </div>
            </div>
            <button type="submit">
              Submit
            </button>
          </form>
        </div>
      ) : (
        <URLsTable />
      )}
    </div>
  )
}

export default App
