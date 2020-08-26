import React from 'react';
import NavBar from '../Nav/Nav.js';
import VideoControls from './VideoControls.js';
import VideoInfo from './VideoInfo.js';
import VideoPlayer from './VideoPlayer.js';
import testData from '../testVideoData.json'

class VideoPage extends React.Component
{
    constructor(props)
    {
        super(props);
        let params = new URLSearchParams(document.location.search.substring(1));
        let currentId = parseInt(params.get("id"));
        this.state =
        {
            videoId: currentId
        }
    }

    render()
    {
        // Use to send to php: const videoId = this.state.videoId;
        var videoData = testData[0];
        var siblings = testData[1];
        return(
            <div style={{height:"100%"}}>
                <NavBar/>
                <VideoInfo CurrentVideo={videoData} OtherVideos={siblings}/>
                <VideoPlayer VideoLocation={videoData.Location}/>
                <VideoControls Parent={videoData.Parent_Id}/>
            </div>
        );
    }
}

export default VideoPage;