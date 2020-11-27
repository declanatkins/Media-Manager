import React, {useState, useEffect} from 'react'
import {Link} from 'react-router-dom'
import './NavBar.css'


function NavBar() {
    const [click, setClick] = useState(false)
    const [button, setButton] = useState(true)
    
    const handleMenuCLick = () => setClick(!click);
    const closeMobileMenu = () => setClick(false);

    const showButton = () => {
        if (window.innerWidth < 960) {
            setButton(false);
        }
        else {
            setButton(true);
        }
    }

    useEffect(() => {
        showButton();
    }, [])
    window.addEventListener('resize', showButton)

    return (
        <>
            <nav className="navbar">
                <div className="navbar-container">
                    <Link to="/" className="navbar-logo" onClick={closeMobileMenu}>
                        Media App <i className="fab fa-typo3" />
                    </Link>
                    <div className="menu-icon" onClick={handleMenuCLick}>
                        <i className={click ? 'fas fa-times' : 'fas fa-bars'} />
                    </div>
                    <ul className={click ? 'nav-menu active' : 'nav-menu'}>
                        <li className="nav-item">
                            <Link to="/games" className="nav-links" onClick={closeMobileMenu}>
                                Games
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/music" className="nav-links" onClick={closeMobileMenu}>
                                Music
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/movies" className="nav-links" onClick={closeMobileMenu}>
                                Movies
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/sign-up" className="nav-links-mobile" onClick={closeMobileMenu}>
                                Sign Up
                            </Link>
                        </li>
                    </ul>
                </div>
            </nav>
        </>
    )
}

export default NavBar
