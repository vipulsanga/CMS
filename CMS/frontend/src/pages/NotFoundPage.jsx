import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';

const NotFoundPage = () => (
  <div>
    <Navbar />
    <div className="container py-5 text-center">
      <h1 className="display-6 mb-3">404 - Page Not Found</h1>
      <p className="text-muted mb-4">The page you are looking for does not exist.</p>
      <Link className="btn btn-primary" to="/">
        Back to Articles
      </Link>
    </div>
  </div>
);

export default NotFoundPage;
