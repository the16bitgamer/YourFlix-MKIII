import React from 'react';
import Nav from '../Nav/Nav';
import Fetch from '../Database/Fetch';
import ProgramTable from '../Programs/ProgramTable';

class NewPage extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state =
        {
            programs: [],
            pulled: false
        };
        this.PullReturn = this.PullReturn.bind(this);
        Fetch("/php/GetLatestPrograms.php", this.PullReturn);
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
                    <ProgramTable Programs={programs} SortByName={false}/>
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

export default NewPage