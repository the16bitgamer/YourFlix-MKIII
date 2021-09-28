import React from 'react';
import './css/yf-program.css';
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
            date: Date.parse(program.Program_Last_Updated),
            link: props.link,
            width: width
        }
    }

    render()
    {
        const progName = this.state.name;
        const link = this.state.link;
        const img = this.state.img;
        var currentDate = new Date();
        const isNew = this.state.date >= currentDate.setMonth(currentDate.getMonth() - 1);

        return(
            <a href={link} className="Program" style={{cursor: "pointer"}}>
                <ProgramImage name={progName} img={img} isNew={isNew}/>
                <h4 className="ProgramName">{progName}</h4>
            </a>
        );
    }
}

export default Program;