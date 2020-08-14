import React from 'react'
import './css/yf-program.css'
import sizeImg from './PS_0-Clear.png'

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
            width: width
        }
        this.ProgramImg = this.ProgramImg.bind(this);
    }
    
    GetShowColor()
    {
        const progName = this.state.name;
        var colour = 0;
        for (var n = 0, l = progName.length; n < l; n ++) 
        {
		    var hex = Number(progName.charCodeAt(n));
		    colour += hex;
        }
        return colour.toString(16);
    }

    ProgramImg(props)
    {
        const progName = props.name;
        const showImg = props.img;
        const showColor = this.GetShowColor();
        if(showImg !== "" && showImg)
        {
            return(
                <div className="ImageBox">
                    <img src={this.state.img} alt={progName}/>
                </div>
            );
        }
        else
        {
            return(
                <div className="ImageBox" style={{backgroundColor:"#"+showColor}}>
                    <img src={sizeImg} alt={progName}/>
                    <div className="TextCentered">{progName.substring(0, 2).toUpperCase()}</div>
                </div>
            );
        }
    }

    render()
    {
        const progName = this.state.name;
        const progId = this.state.id;
        const img = this.state.img;
        return(
        <a href={"/show?id="+progId}>
            <div className="Program">
                <this.ProgramImg name={progName} img={img}/>
                <h4 className="ProgramName">{progName}</h4>
            </div>
        </a>
        );
    }
}

export default Program;