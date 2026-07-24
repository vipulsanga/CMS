import React from 'react';

const formatDate = (dateString) => {
  if (!dateString) return '';

  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
};

const ArticleList = ({ articles = [] }) => {
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
        <h1 className="mb-4">Latest Articles</h1>
        <div className="row">
          {articles.length > 0 ? (
            articles.map((article) => (
              <div className="col-md-6 col-lg-4 mb-4" key={article.id}>
                <div className="card h-100">
                  <div className="card-body">
                    <h5 className="card-title">{article.title}</h5>
                    <p className="card-text text-muted">
                      Published on {formatDate(article.created_at)}
                    </p>
                    <a href={`/articles/${article.id}`} className="btn btn-primary">
                      Read More
                    </a>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="col-12">
              <p className="text-center">No articles available yet.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ArticleList;
