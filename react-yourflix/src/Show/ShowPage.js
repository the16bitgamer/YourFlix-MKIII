import React from 'react';
import ShowBar from './ShowBar';
import ShowDescription from './ShowDescription';
import Fetch from '../Database/Fetch';
import Nav from '../Nav/Nav';
import ShowTable from './ShowTable';

class ShowPage extends React.Component
{
    constructor(props)
    {
        super(props);
        let params = new URLSearchParams(document.location.search.substring(1));
        let currentId = parseInt(params.get("id"));
        this.state =
        {
            program: [],
            contentFolder: [],
            currId: currentId,
            pulled: false
        };
        this.ChangeFolder = this.ChangeFolder.bind(this);
        this.ShowReturn = this.ShowReturn.bind(this);
        this.SearchShow(currentId);
    }

    SearchShow(showId)
    {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                { 
                    Id: showId
                })
        };

        Fetch("/php/PullShow.php", this.ShowReturn, requestOptions);
    }

    ShowReturn(results)
    {
        this.setState(
            {
                program: JSON.parse(results[0]),
                contentFolder: results[1],
                pulled: true
            });
    }

    ChangeFolder(newId)
    {
        const progId = this.state.program.Id;
        window.history.replaceState(null, null, "/Show?id="+newId);
        this.SearchShow(newId);
        this.setState(
            {
                currId: newId
            });
    }

    render()
    {
        const program = this.state.program;
        const content = this.state.contentFolder;
        const pulled = this.state.pulled;
        if(pulled)
        {
            return(
                <div>
                    <Nav/>
                    <ShowBar ProgramId={program.Id} currentId={this.state.currId} Folders={content} function={this.ChangeFolder}/>
                    <ShowDescription Program={program}/>
                    <ShowTable currentId={this.state.currId}/>
                </div>
            );
        }
        else
        {
            return(
                <div>
                    <Nav/>
                    <h3>Loading...</h3>
                </div>
            );
        }
    }
}

export default ShowPage;