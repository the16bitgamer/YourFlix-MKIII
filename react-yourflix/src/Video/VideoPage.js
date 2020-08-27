import React from 'react';
import NavBar from '../Nav/Nav.js';
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
        this.GetHeights = this.GetHeights.bind(this);
        this.navBarRef = React.createRef();
        this.videoInfoRef = React.createRef();
    }

    GetHeights()
    {
        var navHeight = this.navBarRef.current.offsetHeight;
        var infoHeight = this.videoInfoRef.current.offsetHeight;
        return navHeight + infoHeight;
    }

    render()
    {
        // Use to send to php: const videoId = this.state.videoId;
        var videoData = testData[0];
        var siblings = testData[1];
        return(
            <div style={{height:"100%"}}>
                <div ref={this.navBarRef}>
                    <NavBar/>
                    </div>
                <div ref={this.videoInfoRef} >
                    <VideoInfo CurrentVideo={videoData} OtherVideos={siblings}/>
                </div>
                <VideoPlayer VideoData={videoData} Heights={this.GetHeights}/>
            </div>
        );
    }
}

export default VideoPage;