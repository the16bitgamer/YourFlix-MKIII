import React from 'react';
import Nav from '../Nav/Nav';
import Fetch from '../Database/Fetch';
import ProgramTable from '../Programs/ProgramTable';

class ProgramPage extends React.Component
{
    constructor(props)
    {
        super(props);
        
        let params = new URLSearchParams(document.location.search.substring(1));
        let currentChannel = params.get("channel")+"";
        this.state =
        {
            programs: [],
            pulled: false
        };
        this.PullReturn = this.PullReturn.bind(this);
        if(currentChannel === "null")
        {
            console.log("Am Null");
            Fetch("/php/GetChannelPrograms.php", this.PullReturn);
        }
        else
        {
            console.log("Am not Null");
            this.GetChannelProgram(currentChannel);
        }
    }

    GetChannelProgram(CHANNEL)
    {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                { 
                    Channel_Id: CHANNEL
                })
        };
        Fetch("/php/GetChannelPrograms.php", this.PullReturn, requestOptions);
    }

    PullReturn(results)
    {
        this.setState(
            {
                programs: results,
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
                    <ProgramTable Programs={programs} SortByName={true}/>
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

export default ProgramPage