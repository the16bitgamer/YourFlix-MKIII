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
                <input type="image" className="FloatRight NavBarHamSize" alt="Options" src={menu}/>
            </th>
        );
    }

    ChannelOptions()
    {
        return (
            <tr className="ChannelBar">
                <th>
                    <a href="/Programs"><h3>All</h3></a>
                </th>
                <th>
                    <a href="/Programs?channel=Films"><h3>Films</h3></a>
                </th>
                <th>
                    <a href="/Programs?channel=Shows">
                        <h3>Shows</h3>
                    </a>
                </th>
            </tr>
        );
    }

    render()
    {
        return(
            <div className="TopBar">
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
                <table className="ChannelBar">                
                    <tbody>
                        <tr>
                            <th>
                                <a href="/New">
                                    <div>New</div>
                                </a>
                            </th>
                            <th>
                                <a href="/Programs">                                    
                                    <div>All</div>
                                </a>
                            </th>
                            <th>
                                <a href="/Programs?channel=Films">
                                    <div>Films</div>
                                </a>
                            </th>
                            <th>
                                <a href="/Programs?channel=Shows">
                                    <div>Shows</div>
                                </a>
                            </th>
                        </tr>
                    </tbody>
                </table>
            </div>
        )
    }
}

export default Nav