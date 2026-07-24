import React from 'react';

const formatDateTime = (value) => {
  if (!value) return '';

  return new Date(value).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });
};

const ArticleDetail = ({ article }) => {
  if (!article) {
    return null;
  }

  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container">
          <a className="navbar-brand" href="/">
            CMS Articles
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item">
                <a className="btn btn-light btn-sm ms-2" href="/admin/" target="_blank" rel="noopener noreferrer">
                  Admin Panel
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <div className="container mt-4">
        <article>
          <h1 className="mb-3">{article.title}</h1>
          <div className="mb-4">
            <small className="text-muted">
              Created: {formatDateTime(article.created_at)} | Updated: {formatDateTime(article.updated_at)}
            </small>
          </div>
          <div className="content">{article.content}</div>
        </article>
        <div className="mt-4">
          <a href="/" className="btn btn-secondary">
            ← Back to 
          </a>
        </div>
      </div>
    </div>
  );
};

export default ArticleDetail;
