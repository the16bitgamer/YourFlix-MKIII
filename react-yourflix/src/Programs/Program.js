import React from 'react';
import './css/yf-program.css';
import Fetch from '../Database/Fetch';
import ProgramImage from './ProgramImage';

class Program extends React.Component
{
    constructor(props)
    {
        super(props)
        const program = props.program;
        const width = props.width;

        this.state =
        {
            name: program.Name,
            id: program.Id,
            img: "",
            link: props.link,
            width: width
        }
        this.FetchLink = this.FetchLink.bind(this);
        this.LinkResults = this.LinkResults.bind(this);
    }

    FetchLink()
    {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                { 
                    Id: this.state.link
                })
        };
        
        Fetch("/php/ProgramLink.php", this.LinkResults, requestOptions);
    }

    LinkResults(results)
    {
        window.open(results,"_self");
    }


    render()
    {
        const progName = this.state.name;
        const link = this.state.link;
        const img = this.state.img;
        const programId = this.state.id;
        return(
            <div className="Program" style={{cursor: "pointer"}} onClick={this.FetchLink}>
                <ProgramImage name={progName} img={img}/>
                <h4 className="ProgramName">{progName}</h4>
            </div>
        );
    }
}

export default Program;