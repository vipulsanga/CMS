import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { apiUrl } from '../config';

const ArticleDetailPage = () => {
  const { id } = useParams();
  const [article, setArticle] = useState(null);

  useEffect(() => {
    fetch(apiUrl(`/api/articles/${id}/`))
      .then(async (response) => {
        const contentType = response.headers.get('content-type') || '';
        if (!response.ok) {
          const text = contentType.includes('application/json') ? await response.json() : await response.text();
          throw new Error(typeof text === 'string' ? text : text.error || 'Failed to load article');
        }

        if (contentType.includes('application/json')) {
          return response.json();
        }

        const text = await response.text();
        throw new Error(text || 'Failed to load article');
      })
      .then((data) => setArticle(data))
      .catch((error) => {
        console.error('Failed to load article', error);
        setArticle({ title: 'Article unavailable', content: error.message || 'The article could not be loaded.' });
      });
  }, [id]);

  if (!article) {
    return null;
  }

  return (
    <div>
      <Navbar />
      <div className="container mt-4">
        <article>
          <h1 className="mb-3">{article.title}</h1>
          <div className="mb-4">
            <small className="text-muted">Created: {article.created_at}</small>
          </div>
          <div className="content">{article.content}</div>
        </article>
        <div className="mt-4">
          <Link to="/" className="btn btn-secondary">
            ← Back to Articles
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ArticleDetailPage;
