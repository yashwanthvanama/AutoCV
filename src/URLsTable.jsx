import { useState, useEffect } from 'react'
import './URLsTable.css'

function URLsTable() {
  const [urls, setUrls] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchUrls()
  }, [])

  const fetchUrls = async () => {
    setLoading(true)
    setError('')
    
    try {
      const response = await fetch('http://localhost:8000/api/urls')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      console.log('URLs from database:', data)
      setUrls(data.urls || [])
      
    } catch (err) {
      console.error('Error fetching URLs:', err)
      setError(`Failed to load URLs: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id, url) => {
    const preview = url.length > 100 ? url.substring(0, 100) + '...' : url
    if (!window.confirm(`Are you sure you want to delete this text?\n\n${preview}`)) {
      return
    }
    
    try {
      const response = await fetch(`http://localhost:8000/api/urls/${id}`, {
        method: 'DELETE'
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      console.log('Delete response:', data)
      
      // Refresh the URLs list after successful deletion
      await fetchUrls()
      
    } catch (err) {
      console.error('Error deleting URL:', err)
      alert(`Failed to delete URL: ${err.message}`)
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="urls-table-container">
        <div className="loading">Loading URLs...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="urls-table-container">
        <div className="error-message">{error}</div>
        <button onClick={fetchUrls} className="retry-button">
          Retry
        </button>
      </div>
    )
  }

  return (
    <div className="urls-table-container">
      <div className="table-header">
        <h2>Submitted Text Content</h2>
        <div className="table-info">
          <span className="count-badge">{urls.length} total</span>
          <button onClick={fetchUrls} className="refresh-button">
            ↻ Refresh
          </button>
        </div>
      </div>

      {urls.length === 0 ? (
        <div className="empty-state">
          <p>No text submissions yet.</p>
          <p>Submit text using the form to see it here!</p>
        </div>
      ) : (
        <div className="table-wrapper">
          <table className="urls-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Content</th>
                <th>ID</th>
                <th>Submitted At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {urls.map((urlRecord, index) => (
                <tr key={urlRecord.id}>
                  <td className="index-cell">{index + 1}</td>
                  <td className="url-cell">
                    <div className="content-preview" title={urlRecord.url}>
                      {urlRecord.url.length > 100 
                        ? urlRecord.url.substring(0, 100) + '...' 
                        : urlRecord.url}
                    </div>
                  </td>
                  <td className="id-cell">
                    <code>{urlRecord.id}</code>
                  </td>
                  <td className="date-cell">
                    {formatDate(urlRecord.submitted_at)}
                  </td>
                  <td className="actions-cell">
                    <button 
                      onClick={() => handleDelete(urlRecord.id, urlRecord.url)}
                      className="delete-button"
                      title="Delete this URL"
                    >
                      🗑️ Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default URLsTable
