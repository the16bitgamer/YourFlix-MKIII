import React from 'react';
import searchIcon from './img/SearchIcon.svg';
import Fetch from '../Database/Fetch';
import './css/yf-search.css';

const searchLimit = 5;

class SearchBar extends React.Component
{

    constructor(props) {
        super(props);
        this.state = 
        {
            search: "",
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
        window.open(results,"_self");
    }

    searchInput(event)
    {
        this.setState({search: event.target.value});
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                { 
                    query: event.target.value
                })
        };
        
        Fetch("/php/SearchForProgram.php", this.SearchReturn, requestOptions);
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
        const search = this.state.search;
            
        if(hasResults)
        {
            for(var i = 0; i < len; i++)
            {
                const obj = JSON.parse(progs[i]);
                var programLink = "/Show?id=" + obj.First_Folder;

                if(obj.Num_Content == 1)
                {
                    programLink = "/Video?id=" + obj.First_Content;
                }
                
                searchItems.push(
                    <a href={programLink} key={obj.Program_Id}>
                            {obj.Program_Name}
                    </a>);
                    
                if(i >= searchLimit-2 && len > searchLimit)
                    break;
            }
            
            if(len > searchLimit)
            {
                searchItems.push(
                    <a href={"/Search?query="+search} key={"More"}>
                            {"+" + (len - searchLimit + 1) + " More Results"}
                    </a>);
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