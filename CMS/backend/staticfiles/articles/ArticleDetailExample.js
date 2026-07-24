import React from 'react';
import ReactDOM from 'react-dom/client';
import ArticleDetail from './ArticleDetail';

const article = {
  id: 1,
  title: 'Sample Article',
  content: 'This is a sample article rendered with React.',
  created_at: '2026-07-21T10:00:00Z',
  updated_at: '2026-07-21T10:30:00Z',
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<ArticleDetail article={article} />);
