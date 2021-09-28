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
            progressBarRef: props.ProgressBarRef,
            timerRef: props.TimerRef,
            UpdateTimeLine: props.UpdateTimeLine,
            backLink: props.Link,
            isPaused: props.VideoPaused,
            play: props.PlayFunc,
            seek: props.SeekFunc,
            full: props.FulllScreenFunc,
            isFullScreen: props.isFullScreen
        }
        this.UpdatingTimeLine = this.UpdatingTimeLine.bind(this);
    }

    UpdatingTimeLine(event)
    {
        this.state.UpdateTimeLine(event.target.value);
    }
    
    shouldComponentUpdate(nextProps) 
    {
        if(this.state.isPaused !== nextProps.VideoPaused)
        { 
            this.setState({ isPaused: nextProps.VideoPaused});
        }
        if(this.state.isFullScreen !== nextProps.isFullScreen)
        { 
            this.setState({ isFullScreen: nextProps.isFullScreen});
        }
        return true;
    }

    render()
    {
        const returnPage = this.state.backLink;
        const playButt = this.state.play;
        const seekButt = this.state.seek;
        const isFull = this.state.full;
        const progressBarRef = this.state.progressBarRef;
        const timerRef = this.state.timerRef;
        var playImg = PauseButton;
        var positionSet = "relative";
        var color = "gray";
        if(this.state.isFullScreen)
        {
            positionSet = "absolute";
            var color = "transparent";
        }
        if(this.state.isPaused)
        {
            playImg = PlayButton;
        }
        return(
            <div className="VideoController" style={{position: positionSet, bottom: "0", left: "0", backgroundColor: color}}>
                <tr className="VideoTimeBar">
                    <th className="VideoProgressBar">
                        <input className="ProgressBar" type="range" min="0" max="100" ref={progressBarRef} onChange={this.UpdatingTimeLine}/>
                    </th>
                    <th className="VideoTimeRemain" ref={timerRef}>
                        00:00/00:00
                    </th>
                </tr>
                <a href={returnPage}>
                    <button className="BackButton">
                        <img alt="Back" src={BackArrow}/>
                    </button>
                </a>
                <button className="FullScreen" onClick={isFull}>
                    <img alt="Full Screen" src={ExpandButton}/>
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