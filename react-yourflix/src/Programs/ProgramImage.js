import React from 'react';
import sizeImg from './PS_0-Clear.png'

class ProgramImage extends React.Component
{
    constructor(props)
    {
        super(props);
        const programName = props.name;
        const programImg = props.img;
        const programNew = props.isNew;

        this.state =
        {
            name: programName,
            img: programImg,
            isNew: programNew
        }
        this.GetNewBadge = this.GetNewBadge.bind(this);
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

    addDefaultSrc(ev){
        ev.target.src = sizeImg;
      }

    GetNewBadge()
    {
        if(this.state.isNew)
            return <h4 className="NewTextBadge">New</h4>;
        return <div/>
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
                    <this.GetNewBadge/>
                    <img onError={this.addDefaultSrc} src={this.state.img} alt={progName}/>
                </div>
            );
        }
        else
        {
            return(
                <div className="ImageBox" style={{backgroundColor:"#"+showColor}}>
                    <this.GetNewBadge/>
                    <img src={sizeImg} alt={progName}/>
                </div>
            );
        }
    }
}

export default ProgramImage;