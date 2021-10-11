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
            pulledFullScreen: props.PulledFullScreen,
            isFullScreen: false,
            fullScreenEnabled: false,
            heightSet: false,
            videoSet: false,
            videoLoaded: false,
            isPaused: true,
            updateHight: false,
            hideTimmer: 0,
            touchTimmer: 0,
            touchPos: 0,
            touchCount : 0,
            newTime: 0,
            showBar: true,
            height: 0,
            controlHeight: 0,
            hideDelay: 3000,
            skipDelay: 1000
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
    
    shouldComponentUpdate(nextProps) 
    {
        if(this.state.pulledFullScreen !== nextProps.PulledFullScreen)
        {
            this.setState({pulledFullScreen: nextProps.PulledFullScreen});
            this.updateWindowDimensions();
        }
        return true;
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
            //Detects Fullscreeen
            document.onFullscreenChange = (event) => {
                if (document.fullscreenElement)
                {
                    this.setState({isFullScreen:true});
                }
                else
                {                    
                    this.setState({isFullScreen:false});
                    if(this.state.fullScreenEnabled)
                        this.ToggleFullScreen();
                }
                this.updateWindowDimensions();
              }
            var video = this.videoRef.current;
            var progressBar = this.progressBarRef.current;

            if(progressBar && !this.state.videoLoaded)
            {
                progressBar.value = "0";
            }

            var updateBar = true;

            //When the video element is ready
            if(video)
            {
                video.onloadeddata = (event) => {
                    progressBar.max = video.duration+"";
                    this.setState({videoLoaded:false});
                }

                //Progress Bar Update
                progressBar.addEventListener('touchstart', (event) => {
                    updateBar = false;
                });
                progressBar.addEventListener("touchend", (event) =>
                {
                    var newTime = this.state.newTime;
                    updateBar = true;
                    video.currentTime = newTime;
                    this.setState({ hideTimmer: Date.now() + this.state.hideDelay});
                });
                progressBar.onmousedown = (event) =>
                {
                    updateBar = false;
                }
                progressBar.onmouseup = (event) =>
                {
                    var newTime = this.state.newTime;
                    updateBar = true;
                    video.currentTime = newTime;
                    this.setState({ hideTimmer: Date.now() + this.state.hideDelay});
                }

                //Video Player Touch Controls
                var onTouch = false;
                video.addEventListener('touchstart', (event) =>
                {
                    var touch = event.touches[0] || event.changedTouches[0];
                    var x = Math.floor(touch.pageX / (video.offsetWidth/3));
                    var prevTouch = this.state.touchPos === x;                    
                    this.setState({touchPos: x});
                    if(!prevTouch)
                    {
                        this.setState(
                            {
                                touchTimmer: Date.now() + this.state.skipDelay,
                                touchCount: 0                                
                            });
                    }
                    onTouch = true;
                });
                video.addEventListener('touchend', (event) =>
                {
                    console.log("Hello World");
                    var touch = event.touches[0] || event.changedTouches[0];
                    var x = Math.floor(touch.pageX / (video.offsetWidth/3));
                    
                    var counter = this.state.touchCount;
                    var active = counter > 0;

                    if(active)
                    {
                        this.setState({ touchTimmer: Date.now() + this.state.skipDelay });
                        switch(this.state.touchPos)
                        {
                            //Left Side
                            case 0:
                                this.SeekButton(-10);
                                break;
                            //Right Side
                            case 2:
                                this.SeekButton(10);
                                break;
                        }
                    }                   
                    this.setState(
                        {
                            hideTimmer: Date.now() + this.state.hideDelay,
                            showBar: true,
                            touchCount: counter + 1
                        });
                });

                //Mouse Controls
                video.onclick = (event) =>
                {
                    if(!onTouch)
                    {
                        this.PlayButton();
                    }
                    else
                    {
                        const platform = String(navigator.platform);
                        switch(platform)
                        {
                            case "New Nintendo 3DS":
                            case "PlayStation Vita":
                            case "Nintendo WiiU":
                                this.PlayButton();
                                break;
                        }
                    }
                }
                video.onmousemove = (event) => {
                    if(!onTouch)
                    {
                        this.setState(
                        {
                            hideTimmer: Date.now() + this.state.hideDelay,
                            touchTimmer: Date.now() + this.state.skipDelay,
                            showBar: true
                        });
                    }
                }

                //Updating Progress Bar Text & showing Video Controls deciders
                video.ontimeupdate = (event) =>
                {
                    if(updateBar)
                    {
                        var currentTime = video.currentTime;
                        var isFull = this.state.fullScreenEnabled;
                        progressBar.value = currentTime;
                        
                        var isHours = video.duration >= (3600);
                        this.timerRef.current.innerHTML = this.SecondsToHHMM(currentTime, isHours)+"/"+this.SecondsToHHMM(video.duration, isHours);
                        if(this.state.hideTimmer <= Date.now() && this.state.showBar)
                        {
                            this.setState(
                                {
                                    showBar: false || !isFull,                                    
                                    touchCount: 0
                                });
                        }
                        if(this.state.touchTimmer <= Date.now() && onTouch)
                        {
                            if(this.state.touchCount > 1)
                            {
                                this.setState(
                                    {
                                        showBar: false || !isFull,                                    
                                        touchCount: 0
                                    });
                            }
                            onTouch = false;
                        }
                    }
                }
                //Video Player Events
                video.onpause = (event) =>
                {
                    this.setState(
                        {
                            isPaused:true,
                            showBar: true
                        });
                };
                video.onplay = (event) =>
                {
                    this.setState(
                        {
                            isPaused:false,
                            hideTimmer: Date.now() + this.state.hideDelay
                        });
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
        var bottomHeight = 0;

        const platform = String(navigator.platform);
        var consoleOffSet = 0;
        switch(platform)
		{
            case "New Nintendo 3DS":
            case "PlayStation Vita":
            case "Nintendo WiiU":
                consoleOffSet = 45;
                break;            
                consoleOffSet = 45;
                break;
        }

        if(this.controlRef.current !== null && this.state.controlHeight === 0)
        {
            bottomHeight = this.controlRef.current.offsetHeight;            
            this.setState({controlHeight:bottomHeight});
        }
        else if(!this.state.fullScreenEnabled)
            bottomHeight = this.state.controlHeight;

        this.setState(
            { 
                height: height - topHeight - bottomHeight -consoleOffSet,
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
        this.setState({ hideTimmer: Date.now() + this.state.hideDelay});
        video.currentTime += time;
    }

    FullScreenButton()
    {
        const video = document.documentElement;
        if(!this.state.isFullScreen && !this.state.fullScreenEnabled)
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
        else if(this.state.isFullScreen && this.state.fullScreenEnabled)
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
        this.ToggleFullScreen();
    }

    ToggleFullScreen()
    {
        var video = this.videoRef.current;
        var setFullScreen = !this.state.fullScreenEnabled;
        this.state.FullScreenChange(setFullScreen);
        this.setState(
        {
            fullScreenEnabled: setFullScreen,
            hideTimmer: Date.now + this.state.hideDelay,
            showBar: !setFullScreen
        });
        this.updateWindowDimensions();
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
            const isFullScreen = this.state.fullScreenEnabled;
            if(!this.state.showBar)
            {
                controlHeight = "hidden";
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