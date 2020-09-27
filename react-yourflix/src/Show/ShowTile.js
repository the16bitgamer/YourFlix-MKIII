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
        }
    }

    render()
    {
        var name = this.state.showName;
        const id = this.state.showId;

        return(
            <div>
                <div className="ShowTile">
                    <a href={"/Video?id="+id}>
                        <img className="PlayContent" src={playButton} alt="PlayButton"/>
                    </a>
                    <h2 className="ContentName">{name}</h2>
                </div>
            </div>
        );
    }
}

export default ShowTile;