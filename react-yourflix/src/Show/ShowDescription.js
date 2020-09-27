import React from 'react';
import ProgramImage from '../Programs/ProgramImage';
import './css/yf-ShowDescription.css'

class ShowDescription extends React.Component
{
    constructor(props)
    {
        super(props);

        this.state =
        {
            program: props.Program
        }
    }

    render()
    {
        const program = this.state.program;
        const programName = program.Program_Name;
        const img = program.Img_Location;
        return(
            <div className="ShowDescription">
                <div className="Image">
                    <ProgramImage name={programName} img={img}/>
                </div>
                <h1 className="ShowName">{programName}</h1>
            </div>
        );
    }
}

export default ShowDescription;