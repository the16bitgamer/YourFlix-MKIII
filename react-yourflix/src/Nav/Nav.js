import React from 'react';
import logo from './img/YourFlix.svg';
import menu from './img/Temp Hamburger Buttons.png';
import SearchBar from './SearchBar';
import './css/yf-sizing.css'


class Nav extends React.Component
{
    MenuOption()
    {
        return (            
            <th className="VCenter RowFixed">
                <input type="image" className="FloatRight NavBarHamSize" alt=""/>
            </th>
        );
    }

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
                        <this.MenuOption />
                    </tr>
                </thead>
            </table>
        )
    }
}

export default Nav