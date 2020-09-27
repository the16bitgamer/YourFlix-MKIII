import React from 'react';
import sizeImg from './PS_0-Clear.png'

class ProgramImage extends React.Component
{
    constructor(props)
    {
        super(props);
        const programName = props.name;
        const programImg = props.img;

        this.state =
        {
            name: programName,
            img: programImg
        }
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

    render()
    {
        const progName = this.state.name;
        const showImg = this.state.img;
        const showColor = this.GetShowColor();
        if(showImg)
        {
            return(
                <div className="ImageBox" style={{backgroundColor:"#"+showColor}}>
                    <img src={"http://yourflix.tv/"+this.state.img} alt={progName}/>
                </div>
            );
        }
        else
        {
            return(
                <div className="ImageBox" style={{backgroundColor:"#"+showColor}}>
                    <img src={sizeImg} alt={progName}/>
                </div>
            );
        }
    }
}

export default ProgramImage;