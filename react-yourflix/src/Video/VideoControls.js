import React from 'react';
import BackArrow from '../img/Left-Point Arrow.svg';
import PlayButton from './img/PlayButton.svg';
import PauseButton from './img/PauseButton.svg';
import ExpandButton from './img/ExpandButton.svg';
import TheaterButton from './img/TheaterIcon.svg';
import TheaterOffButton from './img/TheaterOffIcon.svg';
import './css/yf-VideoControls.css';

class VideoControls extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state = 
        {
            backLink: props.Link,
            isPaused: props.VideoPaused,
            play: props.PlayFunc,
            seek: props.SeekFunc,
            full: props.FulllScreenFunc,
            isTheaterOn: props.TheaterOn,
            theaterFunc: props.TheaterFunc
        }
        this.ToggleTheaterView = this.ToggleTheaterView.bind(this);
    }
    
    shouldComponentUpdate(nextProps) 
    {
        if(this.state.isPaused !== nextProps.VideoPaused)
        { 
            this.setState({ isPaused: nextProps.VideoPaused});
        }
        return true;
    }

    ToggleTheaterView()
    {
        this.state.theaterFunc();
        this.setState({ isTheaterOn: !this.state.isTheaterOn});
    }

    render()
    {
        const returnPage = this.state.backLink;
        const playButt = this.state.play;
        const fullButt = this.state.full;
        const seekButt = this.state.seek;
        var playImg = PauseButton;
        var theater = TheaterOffButton;
        if(this.state.isPaused)
        {
            playImg = PlayButton;
        }
        
        if(this.state.isTheaterOn)
        {
            theater = TheaterButton;
        }

        return(
            <div className="VideoController">
                <a href={returnPage}>
                    <button className="BackButton">
                        <img alt="Back" src={BackArrow}/>
                    </button>
                </a>
                <button className="FullScreen" onClick={fullButt}>
                    <img alt="Full Screen" src={ExpandButton}/>
                </button>
                <button className="FullScreen" onClick={this.ToggleTheaterView}>
                    <img alt="Theater Mode" src={theater}/>
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