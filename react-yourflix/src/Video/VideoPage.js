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
        let theaterView = false;
        if ("theaterView" in localStorage)
        {
            theaterView = localStorage.getItem("theaterView") == "true";
        }
        this.state =
        {
            videoId: currentId,
            theaterView: theaterView,
            videoData: [],
            pulled: false
        }
        this.GetHeights = this.GetHeights.bind(this);
        this.navBarRef = React.createRef();
        this.videoInfoRef = React.createRef();
        this.ContentReturn = this.ContentReturn.bind(this);
        this.ToggleTheaterView = this.ToggleTheaterView.bind(this);
        this.GetTheaterMode = this.GetTheaterMode.bind(this);   
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

    GetHeights()
    {
        var navHeight = 0;
        if(!this.state.theaterView){ navHeight = this.navBarRef.current.offsetHeight; }
        var infoHeight = this.videoInfoRef.current.offsetHeight;
        return navHeight + infoHeight;
    }

    ToggleTheaterView()
    {
        var currentView = !this.state.theaterView;
        localStorage.setItem('theaterView', currentView);
        this.setState(
            {
                theaterView: currentView
            });
    }

    GetTheaterMode()
    {
        return this.state.theaterView;
    }

    render()
    {
        // Use to send to php: const videoId = this.state.videoId;
        var videoData = this.state.videoData;
        var pulled = this.state.pulled;
        var theaterView = this.state.theaterView;
        if(pulled)
        {
            var prevVideo = this.state.prevVideo;
            var nextVideo = this.state.nextVideo;
            if(theaterView)
            {
                return(
                    <div class="NightMode">
                        <div key="VideoBar" ref={this.videoInfoRef} >
                            <VideoInfo CurrentVideo={videoData} PrevVideo={prevVideo} NextVideo={nextVideo}/>
                        </div>
                        <VideoPlayer key="VideoPlayer" VideoData={videoData} NextVideo={nextVideo} Heights={this.GetHeights} TheaterOn={theaterView} TheaterFunc={this.ToggleTheaterView}/>
                    </div>
                );
            }
            return(
                <div>
                    <div key="NavBar" ref={this.navBarRef}>
                        <NavBar/>
                    </div>
                    <div key="VideoBar" ref={this.videoInfoRef} >
                        <VideoInfo CurrentVideo={videoData} PrevVideo={prevVideo} NextVideo={nextVideo}/>
                    </div>
                    <VideoPlayer key="VideoPlayer" VideoData={videoData} NextVideo={nextVideo} Heights={this.GetHeights} TheaterOn={theaterView} TheaterFunc={this.ToggleTheaterView}/>
                </div>
            );
            
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