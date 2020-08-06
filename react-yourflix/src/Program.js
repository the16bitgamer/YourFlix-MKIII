import React from 'react'
import './css/yf-program.css'
import sizeImg from './PS_0-Clear.png'

class Program extends React.Component
{
    constructor(props)
    {
        super(props)
        const program = JSON.parse(props.program);
        this.state =
        {
            name: program.Name,
            id: program.Id,
            img: "",
            width: 0,
            height: 0
        };
        this.Programs = this.Programs.bind(this)
        this.ProgramImg = this.ProgramImg.bind(this)
        this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
    }
    
    componentDidMount() {
      this.updateWindowDimensions();
      window.addEventListener('resize', this.updateWindowDimensions);
    }
    
    componentWillUnmount() {
      window.removeEventListener('resize', this.updateWindowDimensions);
    }
    
    updateWindowDimensions() {
      this.setState({ width: window.innerWidth, height: window.innerHeight });
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
        if(this.state.img !== "" && showImg)
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
                <div className="ImageBox" style={{backgroundColor:"#"+this.GetShowColor()}}>
                    <img src={sizeImg} alt={progName}/>
                    <div className="TextCentered">{progName.substring(0, 2).toUpperCase()}</div>
                </div>
            );
        }
    }

    Programs(props)
    {
        const progName = this.state.name;
        const img = props.img;
        return(
        <a href="/show">
            <div className="Program" style={{width:props.width}}>
                <this.ProgramImg name={progName} img={img}/>
                <h4 className="ProgramName">{progName}</h4>
            </div>
        </a>
        );
    }

    render()
    {
        var width = this.state.width;
        var rowWidth = (width/2);
        var rowPadding = 10;
        var colWidth = rowWidth - rowPadding;
        console.log(width + " " + rowWidth)
        return(
            <table className="ProgramTable">
                <tbody>
                    <tr>
                        <th style={{width:rowWidth, padding:rowPadding/2}}>
                            <this.Programs width={colWidth} img={true}/>
                        </th>
                        <th style={{width:rowWidth, padding:rowPadding/2}}>
                            <this.Programs width={colWidth} img={false}/>
                        </th>
                    </tr>
                </tbody>
            </table>
        );
    }

}

export default Program;