import React from 'react';
import ShowBar from './ShowBar';
import ShowDescription from './ShowDescription';
import Nav from '../Nav/Nav';
import testData from "../testshow.json"
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
            program: JSON.parse(testData[0]),
            contentFolder: testData[1],
            currId: currentId
        };
        this.ChangeFolder = this.ChangeFolder.bind(this);
    }

    ChangeFolder(newId)
    {
        const progId = this.state.program.Id;
        window.history.replaceState(null, null, "/Show?id="+newId+"&prog="+progId);
        this.setState(
            {
                currId: newId
            });
    }

    render()
    {
        const program = this.state.program;
        const content = this.state.contentFolder;
        return(
            <div>
                <Nav/>
                <ShowBar ProgramId={program.Id} currentId={this.state.currId} Folders={content} function={this.ChangeFolder}/>
                <ShowDescription Program={program}/>
                <ShowTable currentId={this.state.currId} programId={program.Id}/>
            </div>
        );
    }
}

export default ShowPage;