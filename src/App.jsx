import { useState } from 'react'
import './App.css'

function App() {
  const [url, setUrl] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    console.log('Submitted URL:', url)
    // You can add your URL processing logic here
    alert(`URL submitted: ${url}`)
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
          />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  )
}

export default App
