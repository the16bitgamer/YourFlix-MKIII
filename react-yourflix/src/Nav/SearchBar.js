import React from 'react'
import './css/yf-search.css'

class SearchBar extends React.Component
{
    constructor(props) {
        super(props)
        this.state = 
        {
            search: "",
            items: []
        }
        this.searchInput = this.searchInput.bind(this)
        this.searchSubmit = this.searchSubmit.bind(this)
    }

    searchInput(event)
    {
        this.setState({search: event.target.value})
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
                    items: data
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
                    items: data
                }
            );
            //console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    }

    SearchResults(props)
    {
        const items = props.searched.data;
        const hasResults = items.length > 0;
        const searchItems = items.map((item) =>
        {
            const obj = JSON.parse(item);
            return <a href={"/program?id="+obj.Id}>{obj.Name}</a>; 
        });
            
        if(hasResults)
        {
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
        const data = this.state.items;
        return(
            <div className="dropdown">
                <input className="SearchInput" type="text" value={this.state.search}  onChange={this.searchInput} placeholder="Search Program"/>
                <button onClick={this.searchSubmit} className="SearchButton" value="Submit">Search</button>
                <this.SearchResults searched={{data:data}}/>
            </div>
        );
    }
}

export default SearchBar;