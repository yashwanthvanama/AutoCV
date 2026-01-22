import { useState } from 'react'
import './App.css'

function App() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')
    
    try {
      // Send POST request to FastAPI backend
      const response = await fetch('http://localhost:8000/api/submit-url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url })
      })
      
      // Check if request was successful
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      // Parse the JSON response
      const data = await response.json()
      
      console.log('Response from backend:', data)
      setMessage(`✓ ${data.message}`)
      setUrl('') // Clear the input field
      
    } catch (error) {
      console.error('Error submitting URL:', error)
      setMessage(`✗ Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <h1>URL Submission Form</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="url-input">Enter URL:</label>
          <input
            id="url-input"
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            required
            disabled={loading}
          />
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
  )
}

export default App
