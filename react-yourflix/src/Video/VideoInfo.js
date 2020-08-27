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
            otherVideos: props.OtherVideos
        }

        this.VideoInfoBar = this.VideoInfoBar.bind(this);
    }

    VideoInfoBar(props)
    {
        const currentVideo = this.state.currentVideo;
        const otherVideos = this.state.otherVideos;

        var prevId = "/Show?id="+currentVideo.Parent_Id;
        var nextId = prevId;
        if(otherVideos)
        {
            for(var i = 0; i < otherVideos.length; i++)
            {
                const selectedVideo = JSON.parse(otherVideos[i])
                if(selectedVideo.Id === currentVideo.Id && i+1 < otherVideos.length)
                {
                    nextId = "/Video?id="+JSON.parse(otherVideos[i+1]).Id;
                    break;
                }
                prevId = "/Video?id="+selectedVideo.Id;
            }
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
                        <h1 className="CurrentName">{currentVideo.Name.substring(0,currentVideo.Name.length-4)}</h1>
                </div>
            );
        }
        else
        {
            return(
                <div className="VideoInfoBar">
                        <h1 className="CurrentName">{currentVideo.Name.substring(0,currentVideo.Name.length-4)}</h1>
                </div>
            );
        }
    }

    render()
    {
        return(
            <div>
                <this.VideoInfoBar/>
            </div>
        );
    }
}

export default VideoInfo;