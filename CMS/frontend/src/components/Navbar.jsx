import { Link } from 'react-router-dom';
import { apiUrl } from '../config';

const Navbar = () => {
  const openAdminPanel = () => {
    window.open(apiUrl('/admin/'), '_blank');
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <div className="container">
        <Link className="navbar-brand" to="/">
          CMS Articles
        </Link>
        <div className="collapse navbar-collapse">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <button 
                className="btn btn-light btn-sm ms-2" 
                onClick={openAdminPanel}
                style={{ border: 'none', cursor: 'pointer' }}
              >
                Admin Panel
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
