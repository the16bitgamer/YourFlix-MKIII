import React from 'react';
import logo from './img/YourFlix.png';
import menu from './img/Temp Hamburger Buttons.png';
import SearchBar from './SearchBar';
import './css/yf-sizing.css'


class Nav extends React.Component
{
    render()
    {
        return(
            <table className="NavBar">
                <thead>
                    <tr>
                        <th className="VCenter RowFixed">
                            <a href="/">
                                <img className="FloatLeft NavBarImgSize" alt="YourFlix" src={logo}/>
                            </a>
                        </th>
                        <th className="VCenter">
                            <SearchBar/>
                        </th>
                        <th className="VCenter RowFixed">
                            <input type="image" className="FloatRight NavBarHamSize" alt="Options" src={menu}/>
                        </th>
                    </tr>
                </thead>
            </table>
        )
    }
}

export default Nav