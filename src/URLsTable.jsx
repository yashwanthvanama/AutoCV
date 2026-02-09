import { useState, useEffect } from 'react'
import './URLsTable.css'

function URLsTable() {
  const [submissions, setSubmissions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchSubmissions()
  }, [])

  const fetchSubmissions = async () => {
    setLoading(true)
    setError('')
    
    try {
      const response = await fetch('http://localhost:8000/api/job-descriptions')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      console.log('Job descriptions from database:', data)
      setSubmissions(data.submissions || [])
      
    } catch (err) {
      console.error('Error fetching job descriptions:', err)
      setError(`Failed to load job descriptions: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id, jobDescription) => {
    const preview = jobDescription.length > 100 ? jobDescription.substring(0, 100) + '...' : jobDescription
    if (!window.confirm(`Are you sure you want to delete this job description?\n\n${preview}`)) {
      return
    }
    
    try {
      const response = await fetch(`http://localhost:8000/api/job-descriptions/${id}`, {
        method: 'DELETE'
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      console.log('Delete response:', data)
      
      // Refresh the submissions list after successful deletion
      await fetchSubmissions()
      
    } catch (err) {
      console.error('Error deleting job description:', err)
      alert(`Failed to delete job description: ${err.message}`)
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
        <div className="loading">Loading job descriptions...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="urls-table-container">
        <div className="error-message">{error}</div>
        <button onClick={fetchSubmissions} className="retry-button">
          Retry
        </button>
      </div>
    )
  }

  return (
    <div className="urls-table-container">
      <div className="table-header">
        <h2>Submitted Job Descriptions</h2>
        <div className="table-info">
          <span className="count-badge">{submissions.length} total</span>
          <button onClick={fetchSubmissions} className="refresh-button">
            ↻ Refresh
          </button>
        </div>
      </div>

      {submissions.length === 0 ? (
        <div className="empty-state">
          <p>No job descriptions submitted yet.</p>
          <p>Submit a job description using the form to see it here!</p>
        </div>
      ) : (
        <div className="table-wrapper">
          <table className="urls-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Role</th>
                <th>Job Description</th>
                <th>ID</th>
                <th>Submitted At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {submissions.map((submission, index) => (
                <tr key={submission.id}>
                  <td className="index-cell">{index + 1}</td>
                  <td className="role-cell">
                    <span className="role-badge">{submission.role || 'N/A'}</span>
                  </td>
                  <td className="url-cell">
                    <div className="content-preview" title={submission.job_description}>
                      {submission.job_description.length > 100 
                        ? submission.job_description.substring(0, 100) + '...' 
                        : submission.job_description}
                    </div>
                  </td>
                  <td className="id-cell">
                    <code>{submission.id}</code>
                  </td>
                  <td className="date-cell">
                    {formatDate(submission.submitted_at)}
                  </td>
                  <td className="actions-cell">
                    <button 
                      onClick={() => handleDelete(submission.id, submission.job_description)}
                      className="delete-button"
                      title="Delete this job description"
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
