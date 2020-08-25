import React from 'react';
import './css/yf-search.css';

class SearchBar extends React.Component
{
    constructor(props) {
        super(props);
        this.state = 
        {
            search: "",
            program: [],
            link: []
        }
        this.searchInput = this.searchInput.bind(this);
        this.searchSubmit = this.searchSubmit.bind(this);
        this.SearchResults = this.SearchResults.bind(this);
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

        fetch('/php/SearchDb.php', requestOptions)
        .then(response => response.json())
        .then(data => {
            this.setState(
                {
                    program: data[0],
                    link: data[1]
                }
            );
            //console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });

    }

    searchSubmit()
    {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: this.state.items })
        };

        fetch('/php/SearchDb.php', requestOptions)
        .then(response => response.json())
        .then(data => {
            this.setState(
                {
                    program: data[0],
                    link: data[1]
                }
            );
            //console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    }

    SearchResults()
    {
        const progs = this.state.program;
        const links = this.state.link;
        const len = progs.length;
        const hasResults = len > 0;
        var searchItems = [];
            
        if(hasResults)
        {
            for(var i = 0; i < len; i++)
            {
                const obj = JSON.parse(progs[i]);
                const link = JSON.parse(links[i]);
                searchItems.push(<a key={link} href={link}>{obj.Name}</a>);
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
        return(
            <div className="dropdown">
                <input className="SearchInput" type="text" value={this.state.search}  onChange={this.searchInput} placeholder="Search Program"/>
                <button onClick={this.searchSubmit} className="SearchButton" value="Submit">Search</button>
                <this.SearchResults/>
            </div>
        );
    }
}

export default SearchBar;