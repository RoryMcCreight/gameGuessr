import { NavLink } from 'react-router-dom';

const Navbar = () => (
  <nav>
    <ul>
      <li>
        <NavLink to="/" className="nav-link" activeclassname="active">
          Home
        </NavLink>
      </li>
      <li>
        <NavLink to="/about" className="nav-link" activeclassname="active">
          About
        </NavLink>
      </li>
      <li>
        <NavLink to="/gameboard" className="nav-link" activeclassname="active">
          Game Board
        </NavLink>
      </li>
    </ul>
  </nav>
);

export default Navbar;
