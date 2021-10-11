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
        const checkFull = window.fullScreen || document.webkitIsFullScreen || document.mozFullScreen || false;
        this.state =
        {
            videoId: currentId,
            videoData: [],
            pulled: false,
            isFullScreen: checkFull,
            height: 0
        }
        this.GetHeights = this.GetHeights.bind(this);
        this.navBarRef = React.createRef();
        this.videoInfoRef = React.createRef();
        this.ContentReturn = this.ContentReturn.bind(this);
        this.FullScreenChange = this.FullScreenChange.bind(this);
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
        Fetch("/php/GetContentData.php", this.ContentReturn, requestOptions);
    }

    ContentReturn(results)
    {
        const currentVideo = results[0];
        const otherVideos = results[1];

        var prevId = "/Show?id="+currentVideo.Folder_Id;
        var nextId = prevId;
        if(otherVideos.length > 1)
        {
            for(var i = 0; i < otherVideos.length; i++)
            {
                const selectedVideo = JSON.parse(otherVideos[i])
                if(selectedVideo.Content_Id === currentVideo.Content_Id)
                {
                    if(i+1 < otherVideos.length)
                    {
                        nextId = "/Video?id="+JSON.parse(otherVideos[i+1]).Content_Id;
                    }
                    break;
                }
                prevId = "/Video?id="+selectedVideo.Content_Id;
            }
            console.log(prevId);
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

    FullScreenChange(results)
    {
        var currentView = results;
        this.setState(
            {
                isFullScreen: currentView
            });
    }

    GetHeights()
    {
        if(this.state.isFullScreen)
            return 0;
        else if(this.state.height !== 0)
            return this.state.height;
        
        var navHeight = 0;
        var infoHeight = 0;
        if(this.navBarRef.current !== null)
            navHeight = this.navBarRef.current.offsetHeight;
        if(this.videoInfoRef.current !== null)
            infoHeight = this.videoInfoRef.current.offsetHeight;

        var height = navHeight + infoHeight;
        if(height !== 0)
        this.setState({height: height});
        return height;
    }

    render()
    {
        var videoData = this.state.videoData;
        var pulled = this.state.pulled;
        var isFullScreen = this.state.isFullScreen;

        if(pulled)
        {
            var prevVideo = this.state.prevVideo;
            var nextVideo = this.state.nextVideo;
            if(isFullScreen)
            {
                return(
                    <div>                        
                        <div key="NavBar" ref={this.navBarRef}>
                        </div>
                        <div key="VideoBar" ref={this.videoInfoRef} >
                        </div>
                        <VideoPlayer key="VideoPlayer" VideoData={videoData} NextVideo={nextVideo} Heights={this.GetHeights} FullScreenChange={this.FullScreenChange} PulledFullScreen={this.state.isFullScreen}/>
                    </div>
                );
            }
            else
            {
                return(
                    <div>
                        <div key="NavBar" ref={this.navBarRef}>
                            <NavBar/>
                        </div>
                        <div key="VideoBar" ref={this.videoInfoRef} >
                            <VideoInfo CurrentVideo={videoData} PrevVideo={prevVideo} NextVideo={nextVideo}/>
                        </div>
                        <VideoPlayer key="VideoPlayer" VideoData={videoData} NextVideo={nextVideo} Heights={this.GetHeights} FullScreenChange={this.FullScreenChange} PulledFullScreen={this.state.isFullScreen}/>
                    </div>
                );
            }
        }
        else
        {
            return(
                <div key="NavBar">
                    <NavBar/>
                    <h3>Loading...</h3>
                </div>
            )
        }
        
    }
}

export default VideoPage;