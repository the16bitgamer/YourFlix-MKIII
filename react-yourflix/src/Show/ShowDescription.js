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
            program: props.Program,
            img: ""
        }
    }

    render()
    {
        const programName = this.state.program.Name;
        const img = this.state.img;
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