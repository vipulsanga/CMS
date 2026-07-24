import { useEffect, useState } from 'react';

const AdminPage = () => {
  const [articles, setArticles] = useState([]);
  const [form, setForm] = useState({ id: '', title: '', content: '' });
  const [loading, setLoading] = useState(true);

  const loadArticles = async () => {
    try {
      const response = await fetch('/api/articles/');
      const data = await response.json();
      setArticles(data);
    } catch (error) {
      console.error('Failed to load articles', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadArticles();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const method = form.id ? 'PATCH' : 'POST';
    const url = form.id ? `/api/articles/${form.id}/` : '/api/articles/';

    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      credentials: 'same-origin',
      body: JSON.stringify({ title: form.title, content: form.content }),
    });

    if (response.ok) {
      setForm({ id: '', title: '', content: '' });
      loadArticles();
    }
  };

  const handleDelete = async (id) => {
    const response = await fetch(`/api/articles/${id}/`, {
      method: 'DELETE',
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
      credentials: 'same-origin',
    });

    if (response.ok) {
      loadArticles();
    }
  };

  return (
    <div className="container py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1 className="mb-0">Admin Dashboard</h1>
        <a href="/admin/logout/" className="btn btn-outline-secondary">
          Logout
        </a>
      </div>
      <div className="card mb-4">
        <div className="card-body">
          <h2 className="h5">{form.id ? 'Edit Article' : 'Create Article'}</h2>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <input
                className="form-control"
                placeholder="Title"
                value={form.title}
                onChange={(event) => setForm({ ...form, title: event.target.value })}
                required
              />
            </div>
            <div className="mb-3">
              <textarea
                className="form-control"
                rows="4"
                placeholder="Content"
                value={form.content}
                onChange={(event) => setForm({ ...form, content: event.target.value })}
              />
            </div>
            <div className="d-flex gap-2">
              <button className="btn btn-primary" type="submit">
                {form.id ? 'Save Changes' : 'Create Article'}
              </button>
              {form.id ? (
                <button
                  className="btn btn-secondary"
                  type="button"
                  onClick={() => setForm({ id: '', title: '', content: '' })}
                >
                  Cancel
                </button>
              ) : null}
            </div>
          </form>
        </div>
      </div>

      <div className="card">
        <div className="card-body">
          <h2 className="h5">Articles</h2>
          {loading ? (
            <p>Loading…</p>
          ) : (
            <table className="table table-striped">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Title</th>
                  <th>Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {articles.map((article) => (
                  <tr key={article.id}>
                    <td>{article.id}</td>
                    <td>{article.title}</td>
                    <td>{article.created_at}</td>
                    <td>
                      <button
                        className="btn btn-sm btn-outline-primary me-2"
                        onClick={() => setForm({ id: article.id, title: article.title, content: article.content })}
                      >
                        Edit
                      </button>
                      <button className="btn btn-sm btn-outline-danger" onClick={() => handleDelete(article.id)}>
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(';').shift();
  }
  return '';
}

export default AdminPage;
