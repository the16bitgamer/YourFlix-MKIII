import React from 'react'
import './css/yf-program.css'
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
    }
    

    render()
    {
        const progName = this.state.name;
        const link = this.state.link;
        const img = this.state.img;
        const programId = this.state.id;
        return(
        <a href={link}>
            <div className="Program" id={programId}>
                <ProgramImage name={progName} img={img}/>
                <h4 className="ProgramName">{progName}</h4>
            </div>
        </a>
        );
    }
}

export default Program;