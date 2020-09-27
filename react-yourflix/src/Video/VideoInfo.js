import React from 'react';
import leftArrow from '../img/LeftArrow.svg';
import rightArrow from '../img/RightArrow.svg';
import './css/yf-VideoInfo.css';

class VideoInfo extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state =
        {
            currentVideo: props.CurrentVideo,
            prevVideo: props.PrevVideo,
            nextVideo: props.NextVideo
        }
    }

    render()
    {        
        var currentVideo = this.state.currentVideo;
        var prevId = this.state.prevVideo;
        var nextId = this.state.nextVideo;
        if(prevId && nextId)
        {
            return(
                <div className="VideoInfoBar">
                        <a className="PrevContent" href={prevId}>
                            <button className="IndexButton">
                                <img className="Arrow" alt="<" src={leftArrow}/>                            
                            </button>
                        </a>
                        <a href={nextId} className="NextContent">
                            <button className="IndexButton">
                                <img className="Arrow" alt="Next" src={rightArrow}/>
                            </button>
                        </a>
                        <h1 className="CurrentName">{currentVideo.Content_Name}</h1>
                </div>
            );
        }
        else
        {
            return(
                <div className="VideoInfoBar">
                        <h1 className="CurrentName">{currentVideo.Content_Name}</h1>
                </div>
            );
        }
    }
}

export default VideoInfo;