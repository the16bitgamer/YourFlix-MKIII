import React from 'react';
import Nav from '../Nav/Nav';
import Fetch from '../Database/Fetch';
import ProgramTable from '../Programs/ProgramTable';

class SearchPage extends React.Component
{
    constructor(props)
    {
        super(props);
        let params = new URLSearchParams(document.location.search.substring(1));
        let currentSearch = params.get("query")+"";
        console.log(currentSearch);
        this.state =
        {
            programs: [],
            pulled: false
        };
        this.PullReturn = this.PullReturn.bind(this);
        this.SearchProgram(currentSearch);
    }

    SearchProgram(SEARCH)
    {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                { 
                    query: SEARCH,
                    limit: -1
                })
        };
        Fetch("/php/SearchForProgram.php", this.PullReturn, requestOptions);
    }

    PullReturn(RESULTS)
    {
        console.log(RESULTS);
        this.setState(
            {
                programs: RESULTS,
                pulled: true
            });
    }

    render()
    {
        const pulledResult = this.state.pulled;
        const programs = this.state.programs;

        if(pulledResult)
        {
            return(
                <div>
                    <Nav/>
                    <ProgramTable Programs={programs}/>
                </div>
            )
        }
        return(
            <div>
                <Nav/>
                <h3 style={{color:"white"}}>Loading</h3>
            </div>
        )
    }
}

export default SearchPage