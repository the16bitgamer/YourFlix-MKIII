import React from 'react';
import './css/yf-program.css';
import Fetch from '../Database/Fetch';
import ProgramImage from './ProgramImage';

class Program extends React.Component
{
    constructor(props)
    {
        super(props);
        const program = props.program;
        const width = props.width;

        this.state =
        {
            name: program.Program_Name,
            id: program.Program_Id,
            img: program.Img_Location,
            link: props.link,
            width: width
        }
    }

    render()
    {
        const progName = this.state.name;
        const link = this.state.link;
        const img = this.state.img;

        return(
            <a href={link} className="Program" style={{cursor: "pointer"}}>
                <ProgramImage name={progName} img={img}/>
                <h4 className="ProgramName">{progName}</h4>
            </a>
        );
    }
}

export default Program;