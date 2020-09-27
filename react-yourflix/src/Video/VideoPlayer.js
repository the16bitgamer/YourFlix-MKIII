import React from 'react';
import VideoControls from './VideoControls.js';
import './css/yf-VideoPlayer.css';

class VideoPlayer extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state = 
        {
            videoData: props.VideoData,
            topHeight: props.Heights,
            nextVideo: props.NextVideo,
            heightSet: false,
            videoSet: false,
            isPaused: true,
            height: 0
        };
        this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
        this.PlayButton = this.PlayButton.bind(this);
        this.SeekButton = this.SeekButton.bind(this);
        this.FullScreenButton = this.FullScreenButton.bind(this);
        this.controlRef = React.createRef();
        this.videoRef = React.createRef();
    }

    componentDidUpdate(nextProps) 
    {
        if(nextProps.heightSet !== this.state.heightSet && this.state.videoSet === false)
        {
            var video = this.videoRef.current;
            if(video)
            {
                video.onpause = (event) =>
                {
                    this.setState({isPaused:true});
                };
                video.onplay = (event) =>
                {
                    this.setState({isPaused:false});
                };
                video.onended = (event) =>
                {
                    var nextVideo = this.state.nextVideo;
                    if(nextVideo)
                    {
                        window.open(nextVideo,"_self");
                    }
                }
                this.setState({videoSet:true});
            }
        }
    }
    
    componentDidMount()
    {
        this.updateWindowDimensions();
        window.addEventListener('resize', this.updateWindowDimensions);
    }
    
    componentWillUnmount()
    {
      window.removeEventListener('resize', this.updateWindowDimensions);
    }
    
    updateWindowDimensions() 
    {
        var height = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
        var topHeight = this.state.topHeight();
        var bottomHeight = this.controlRef.current.offsetHeight;
        this.setState(
            { 
                height: height - topHeight - bottomHeight,
                heightSet: true
            });
    }

    PlayButton()
    {
        const video = this.videoRef.current;
        if (video.paused)
        {
            video.play();
        }
        else
        {
            video.pause();
        }
    }

    SeekButton(time)
    {
        const video = this.videoRef.current;
        video.currentTime += time;
    }

    FullScreenButton()
    {
        const video = this.videoRef.current;
        if (video.requestFullscreen) 
        {
            video.requestFullscreen();
        }
        else if (video.mozRequestFullScreen)
        { /* Firefox */
            video.mozRequestFullScreen();
        }
        else if (video.webkitRequestFullscreen)
        { /* Chrome, Safari and Opera */
            video.webkitRequestFullscreen();
        }
        else if (video.msRequestFullscreen)
        { /* IE/Edge */
            video.msRequestFullscreen();
        }
    }

    render()
    {
        const videoData = this.state.videoData;
        const isSet = this.state.heightSet;
        var programLink = "/Show?id=" + videoData.Folder_Id;

        if(videoData.Num_Content == 1)
        {
            programLink = "/";
        }

        if(!isSet)
        {
            return(
            <div ref={this.controlRef}>
                <VideoControls Link={programLink}/>
            </div>);
        }
        else
        {
            const height = this.state.height;
            var isPaused = this.state.isPaused;
            return(
                <div>
                    <video style={{height: height+"px"}} ref={this.videoRef} className='VideoPlayer' controls autoPlay>
                        <source src={ encodeURI(videoData.Content_Location)} type='video/mp4'/>
                    </video>
                    <div ref={this.controlRef}>
                        <VideoControls VideoPaused={isPaused} Link={programLink} PlayFunc={this.PlayButton} SeekFunc={this.SeekButton} FulllScreenFunc={this.FullScreenButton}/>
                    </div>
                </div>
            );
        }
    }
}

export default VideoPlayer;