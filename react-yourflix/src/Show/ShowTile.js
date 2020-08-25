import React from 'react';
import playButton from './img/yf-PlayButton.svg'
import './css/yf-ShowTile.css'

class ShowTile extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state =
        {
            showName: props.Name,
            showId: props.Id,
            progId: props.ProgId
        }
    }

    render()
    {
        var name = this.state.showName;
        name = name.substring(0, name.length - 4);
        const id = this.state.showId;
        const prog = this.state.progId;

        return(
            <div>
                <div className="ShowTile">
                    <a href={"/Video?id="+id+"&prog="+prog}>
                        <img className="PlayContent" src={playButton} alt="PlayButton"/>
                    </a>
                    <h2 className="ContentName">{name}</h2>
                </div>
            </div>
        );
    }
}

export default ShowTile;