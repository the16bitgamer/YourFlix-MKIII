import React from 'react';
import Fetch from '../Database/Fetch';
import NavBar from '../Nav/Nav';
import VideoInfo from './VideoInfo';
import VideoPlayer from './VideoPlayer';

class VideoPage extends React.Component
{
    constructor(props)
    {
        super(props);
        let params = new URLSearchParams(document.location.search.substring(1));
        let currentId = parseInt(params.get("id"));
        this.state =
        {
            videoId: currentId,
            videoData: [],
            pulled: false
        }
        this.GetHeights = this.GetHeights.bind(this);
        this.navBarRef = React.createRef();
        this.videoInfoRef = React.createRef();
        this.ContentReturn = this.ContentReturn.bind(this);        
        this.PullContent(currentId);
    }

    PullContent(currId)
    {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                { 
                    Id: currId
                })
        };
        Fetch("/php/PullContentData.php", this.ContentReturn, requestOptions);
    }

    ContentReturn(results)
    {
        const currentVideo = results[0];
        const otherVideos = results[1];

        var prevId = "/Show?id="+currentVideo.Parent_Id;
        var nextId = prevId;
        if(otherVideos.length > 1)
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
            this.setState(
                {
                    prevVideo: prevId,
                    nextVideo: nextId
                }
            )
        }
        this.setState(
            {
                videoData: currentVideo,
                pulled: true
            });
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
        var videoData = this.state.videoData;
        var pulled = this.state.pulled;
        if(pulled)
        {
            var prevVideo = this.state.prevVideo;
            var nextVideo = this.state.nextVideo;
            return(
                <div>
                    <div ref={this.navBarRef}>
                        <NavBar/>
                        </div>
                    <div ref={this.videoInfoRef} >
                        <VideoInfo CurrentVideo={videoData} PrevVideo={prevVideo} NextVideo={nextVideo}/>
                    </div>
                    <VideoPlayer VideoData={videoData} NextVideo={nextVideo} Heights={this.GetHeights}/>
                </div>
            );
        }
        else
        {
            return(
                <h3>Loading...</h3>
            )
        }
        
    }
}

export default VideoPage;