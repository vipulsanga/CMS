import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { apiUrl } from '../config';

const HomePage = () => {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    fetch(apiUrl('/api/articles/'))
      .then((response) => response.json())
      .then((data) => setArticles(data))
      .catch((error) => console.error('Failed to load articles', error));
  }, []);

  return (
    <div>
      <Navbar />
      <div className="container mt-4">
        <h1 className="mb-4">Latest Articles</h1>
        <div className="row">
          {articles.map((article) => (
            <div className="col-md-6 col-lg-4 mb-4" key={article.id}>
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">{article.title}</h5>
                  <p className="card-text text-muted">Published on {article.created_at}</p>
                  <Link to={`/articles/${article.id}`} className="btn btn-primary">
                    Read More
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default HomePage;
