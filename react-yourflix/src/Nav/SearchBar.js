import React from 'react';
import searchIcon from './img/SearchIcon.svg';
import Fetch from '../Database/Fetch';
import './css/yf-search.css';

class SearchBar extends React.Component
{
    constructor(props) {
        super(props);
        this.state = 
        {
            search: "",
            link: "",
            program: [],
            isVisible: false
        }
        this.searchInput = this.searchInput.bind(this);
        this.SearchReturn = this.SearchReturn.bind(this);
        this.SearchResults = this.SearchResults.bind(this);
        this.FetchLink = this.FetchLink.bind(this);
        this.LinkResults = this.LinkResults.bind(this);
        this.EnterSearch = this.EnterSearch.bind(this);
        this.InputField = React.createRef();
    }

    componentDidMount()
    {
        this.InputField.current.addEventListener("keyup", (event) =>
        {
            if (event.keyCode === 13)
            {
              event.preventDefault();
              this.EnterSearch();
            }
        }); 
    }

    EnterSearch()
    {
        const search = this.state.search;
        window.open("/Search?query="+search,"_self");
    }

    FetchLink(link)
    {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                { 
                    Id: link
                })
        };
        
        Fetch("/php/ProgramLink.php", this.LinkResults, requestOptions);
    }

    LinkResults(results)
    {
        this.setState(
            {
                link: results
            }
        );
    }

    searchInput(event)
    {
        this.setState({search: event.target.value});
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                { 
                    query: event.target.value,
                    limit: 5
                })
        };
        
        Fetch("/php/SearchDb.php", this.SearchReturn, requestOptions);
    }

    SearchReturn(results)
    {
        this.setState(
            {
                program: results
            });
    }

    SearchResults()
    {
        const progs = this.state.program;
        const len = progs.length;
        const hasResults = len > 0;
        var searchItems = [];
            
        if(hasResults)
        {
            for(var i = 0; i < len; i++)
            {
                const obj = JSON.parse(progs[i]);
                const link = obj.Folder_Id;
                
                searchItems.push(
                    <div onClick={()=> this.FetchLink(link)} key={link}>
                        {obj.Name}
                    </div>);
            }

            return(
                <div className="dropdown-content">
                    {searchItems}
                </div>
            );
        }
        return <div className="DropDownNone"/>
    }

    render()
    {
        const search = this.state.search;
        return(
            <div className="dropdown">
                <input className="SearchInput" ref={this.InputField} type="text" value={this.state.search} onChange={this.searchInput} placeholder="Search Program"/>
                <a href={"/Search?query="+search}>
                    <button className="SearchButton" value="Submit">
                        <img alt="search" src={searchIcon}/>
                    </button>
                </a>
                <this.SearchResults/>
            </div>
        );
    }
}

export default SearchBar;