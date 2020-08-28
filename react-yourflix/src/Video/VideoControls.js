import React from 'react';
import BackArrow from '../img/Left-Point Arrow.svg';
import PlayButton from './img/PlayButton.svg';
import PauseButton from './img/PauseButton.svg';
import ExpandButton from './img/ExpandButton.svg';
import './css/yf-VideoControls.css';

class VideoControls extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state = 
        {
            parentId: props.Parent,
            isPaused: props.VideoPaused,
            play: props.PlayFunc,
            seek: props.SeekFunc,
            full: props.FulllScreenFunc
        }
    }
    
    shouldComponentUpdate(nextProps) 
    {
        if(this.state.isPaused !== nextProps.VideoPaused)
        { 
            this.setState({ isPaused: nextProps.VideoPaused});
        }
        return true;
    }

    render()
    {
        const returnPage = "/Show?id="+this.state.parentId;
        const playButt = this.state.play;
        const fullButt = this.state.full;
        const seekButt = this.state.seek;
        var playImg = PauseButton;
        if(this.state.isPaused)
        {
            playImg = PlayButton;
        }

        return(
            <div className="VideoController">
                <a href={returnPage}>
                    <button className="BackButton">
                        <img alt="Back" src={BackArrow}/>
                    </button>
                </a>
                <button className="FullScreen" onClick={fullButt}>
                    <img alt="Back" src={ExpandButton}/>
                </button>
                <div className="MiddleBar">
                    <button className="Skip" onClick={() => seekButt(-10)}>
                        <p>-10</p>
                    </button>
                    <button className="PlayButton" onClick={playButt}>
                        <img alt="Play" src={playImg}/>
                    </button>
                    <button className="Skip" onClick={() => seekButt(+10)}>
                        +10
                    </button>
                </div>
            </div>
        );
    }
}

export default VideoControls;