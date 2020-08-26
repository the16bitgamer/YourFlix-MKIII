import React from 'react';
import BackArrow from '../img/Left-Point Arrow.svg';
import PlayButton from './img/PlayButton.svg';
//import PauseButton from './img/PauseButton.svg';
import ExpandButton from './img/ExpandButton.svg';
import './css/yf-VideoControls.css';

class VideoControls extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state = 
        {
            parentId: props.Parent
        }
    }
    render()
    {
        const returnPage = "/Show?id="+this.state.parentId;
        return(
            <div className="VideoController">
                <a href={returnPage}>
                    <button className="BackButton">
                        <img alt="Back" src={BackArrow}/>
                    </button>
                </a>
                <button className="FullScreen">
                    <img alt="Back" src={ExpandButton}/>
                </button>
                <div className="MiddleBar">
                    <button className="Skip">
                        <p>-10</p>
                    </button>
                    <button className="PlayButton">
                        <img alt="Back" src={PlayButton}/>
                    </button>
                    <button className="Skip">
                        +10
                    </button>
                </div>
            </div>
        );
    }
}

export default VideoControls;