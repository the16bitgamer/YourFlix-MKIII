import React from 'react';
import NavBar from '../Nav/Nav.js';
import VideoControls from './VideoControls.js';
import VideoPlayer from './VideoPlayer.js';

class VideoPage extends React.Component
{
    render()
    {
        return(
            <div style={{height:"100%"}}>
                <NavBar/>
                <VideoPlayer/>
                <VideoControls/>
            </div>
        );
    }
}

export default VideoPage;