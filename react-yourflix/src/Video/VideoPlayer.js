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
            FullScreenChange: props.FullScreenChange,
            isFullScreen: false,
            heightSet: false,
            videoSet: false,
            videoLoaded: false,
            isPaused: true,
            updateHight: false,
            hideTimmer: 0,
            newTime: 0,
            showBar: true,
            height: 0
        };
        this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
        this.PlayButton = this.PlayButton.bind(this);
        this.SeekButton = this.SeekButton.bind(this);
        this.FullScreenButton = this.FullScreenButton.bind(this);
        this.SecondsToHHMM = this.SecondsToHHMM.bind(this);
        this.DisplayTime = this.DisplayTime.bind(this);
        this.UpdateTimeLine = this.UpdateTimeLine.bind(this);
        this.controlRef = React.createRef();
        this.videoRef = React.createRef();
        this.progressBarRef = React.createRef();
        this.timerRef = React.createRef();
    }

    SecondsToHHMM(value, hasHours)
    {
        var seconds = Math.floor(value)%60;
        var minutes = Math.floor(value/60)%60;
        var hours = Math.floor(value/3600);

        if(hasHours)
            return this.DisplayTime(hours)+":"+this.DisplayTime(minutes)+":"+this.DisplayTime(seconds);

        return this.DisplayTime(minutes)+":"+this.DisplayTime(seconds);
    }

    DisplayTime(value)
    {
        if(value > 9)
            return value;
        else
            return "0"+value;
    }

    UpdateTimeLine(value)
    {
        var video = this.videoRef.current;
        this.setState({ newTime: value});
        var isHours = video.duration >= (3600);
        this.timerRef.current.innerHTML = this.SecondsToHHMM(value, isHours)+"/"+this.SecondsToHHMM(video.duration, isHours);
    }

    componentDidUpdate(nextProps) 
    {
        if(nextProps.heightSet !== this.state.heightSet && this.state.videoSet === false)
        {
            
            document.addEventListener('fullscreenchange', (event) => {
                if (document.fullscreenElement)
                {
                  console.log(`Element: ${document.fullscreenElement.id} entered full-screen mode.`);
                  this.state.FullScreenChange(true);
                  this.setState({isFullScreen:true});
                }
                else
                {
                  console.log('Leaving full-screen mode.');
                  this.state.FullScreenChange(false);
                  this.setState({isFullScreen:false});
                }
                this.updateWindowDimensions();
              });

            var video = this.videoRef.current;
            var progressBar = this.progressBarRef.current;

            if(progressBar && !this.state.videoLoaded)
            {
                progressBar.value = 0;
            }

            var updateBar = true;
            if(video)
            {
                video.addEventListener('loadeddata', (event) => {
                    progressBar.max = video.duration;                    
                    this.setState({videoLoaded:false});
                });
                progressBar.addEventListener('touchstart', (event) => {
                    updateBar = false;
                })
                progressBar.addEventListener('touchend', (event) => {
                    
                    var newTime = this.state.newTime;
                    updateBar = true;
                    video.currentTime = newTime;
                    this.setState({ hideTimmer: newTime + 5});
                });
                progressBar.addEventListener('mousedown', (event) => {
                    updateBar = false;
                });
                progressBar.addEventListener('mouseup', (event) =>
                {
                    var newTime = this.state.newTime;
                    updateBar = true;
                    video.currentTime = newTime;
                    this.setState({ hideTimmer: newTime + 5});
                });

                video.addEventListener('mousemove', (event) => {                    
                    this.setState(
                    {
                        hideTimmer: video.currentTime + 5,
                        showBar: true
                    });
                });

                video.addEventListener('timeupdate', (event) =>
                {
                    if(updateBar)
                    {
                        var currentTime = video.currentTime;
                        progressBar.value = currentTime;
                        
                        var isHours = video.duration >= (3600);
                        this.timerRef.current.innerHTML = this.SecondsToHHMM(currentTime, isHours)+"/"+this.SecondsToHHMM(video.duration, isHours);
                        if(this.state.hideTimmer <= currentTime && this.state.showBar && this.state.isFullScreen)
                        {
                            this.setState({ showBar: false });
                        }
                    }
                });
                video.onpause = (event) =>
                {
                    this.setState({isPaused:true});
                    this.setState({ showBar: true});
                };
                video.onplay = (event) =>
                {
                    this.setState({isPaused:false});
                    this.setState({ hideTimmer: video.currentTime + 5});
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

        if(this.state.updateHight === true)
        {
            this.updateWindowDimensions();
            this.setState({updateHight:false});
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
        if(this.state.isFullScreen)
            bottomHeight = 0;
        this.setState(
            { 
                height: height - topHeight - bottomHeight,
                heightSet: true
            });
        console.log("Height = " + topHeight);
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
        this.setState({ hideTimmer: video.currentTime + time + 5});
        video.currentTime += time;
    }

    FullScreenButton()
    {
        const video = document.documentElement;
        const checkFull = window.fullScreen || document.webkitIsFullScreen || document.mozFullScreen || false;
        if(!checkFull)
        {
            if (video.requestFullscreen)
            {
                video.requestFullscreen();
            }
            else if (video.mozRequestFullScreen) /* Firefox */
            {
                video.mozRequestFullScreen();
            }
            else if (video.webkitRequestFullscreen) /* Chrome, Safari and Opera */
            {
                video.webkitRequestFullscreen();
            }
            else if (video.msRequestFullscreen) /* IE/Edge */
            {
                video.msRequestFullscreen();
            }
        }
        else
        {
            if (document.exitFullscreen)
            {
                document.exitFullscreen();
            }
            else if (document.webkitExitFullscreen) /* Safari */
            {
                document.webkitExitFullscreen();
            }
            else if (document.msExitFullscreen) /* IE11 */
            {    
                document.msExitFullscreen();
            }
        }
    }

    render()
    {
        const videoData = this.state.videoData;
        const isSet = this.state.heightSet;
        var programLink = "/Show?id=" + videoData.Folder_Id;
        var controlHeight = "visible";

        if(videoData.Num_Content === 1)
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
            const isFullScreen = this.state.isFullScreen;
            if(!this.state.showBar)
            {
                controlHeight = "hidden";
                console.log("change height")
            }

            return(
                <div>
                    <video style={{height: height+"px"}} ref={this.videoRef} className='VideoPlayer' autoPlay>
                        <source src={ encodeURI(videoData.Content_Location)} type='video/mp4'/>
                    </video>
                    <div style={{visibility: controlHeight}} className='ControlsUI' ref={this.controlRef}>
                        <VideoControls ProgressBarRef={this.progressBarRef} TimerRef={this.timerRef} UpdateTimeLine={this.UpdateTimeLine} VideoPaused={isPaused} Link={programLink} PlayFunc={this.PlayButton} SeekFunc={this.SeekButton} FulllScreenFunc={this.FullScreenButton} isFullScreen={isFullScreen}/>
                    </div>
                </div>
            );
        }
    }
}

export default VideoPlayer;