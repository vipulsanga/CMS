import React from 'react';
import ReactDOM from 'react-dom/client';
import ArticleList from './ArticleList';

const sampleArticles = [
  {
    id: 1,
    title: 'Hello World',
    created_at: '2026-07-21T10:00:00Z',
  },
  {
    id: 2,
    title: 'React in Django',
    created_at: '2026-07-20T10:00:00Z',
  },
];

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<ArticleList articles={sampleArticles} />);
