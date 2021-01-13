import React from 'react';
import BackArrow from '../img/Left-Point Arrow.svg';
import leftArrow from '../img/LeftArrow.svg';
import rightArrow from '../img/RightArrow.svg';
import './css/yf-ShowBar.css';

class ShowBar extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state =
        {
            progId: props.ProgramId,
            currId: props.currentId,
            folders: props.Folders,            
            func: props.function
        }
        this.FolderBar = this.FolderBar.bind(this);
    }

    shouldComponentUpdate(nextProps) 
    {
        if(this.state.currId !== nextProps.currentId)
        {
            this.setState(
                {
                    currId: nextProps.currentId
                }
            );
            return true;
        }
        return false;
    }

    FolderBar(props) 
    {
        const folders = JSON.parse(props.folders);
        var dropDown = [];
        const currentId = props.currentId;
        var prevId = 0;
        var nextId = 0;
        var currentFolder = "";
        for(var i = 0; i < folders.length; i++)
        {
            const folderData = JSON.parse(folders[i]);

            dropDown.push(
                <div key={folderData.Folder_Id} tabindex="-1" onClick={() => this.state.func(folderData.Folder_Id)}>{folderData.Folder_Name}</div>
            )

            if(parseInt(folderData.Folder_Id) === currentId)
            {
                currentFolder = folderData.Folder_Name;                
                var last = (i-1+folders.length)%folders.length;
                var lastData = JSON.parse(folders[last]);
                prevId = lastData.Folder_Id;
                var next = (i+1)%folders.length;
                var nextData = JSON.parse(folders[next]);
                nextId = nextData.Folder_Id;
            }
        }

        return (
            <div className="FolderBar">
                <button key="Back" className="toggleBtn" onClick={() => this.state.func(prevId)}>
                    <img alt="<" src={leftArrow}/>
                </button>
                <div className="showDropDown" ontouchstart="">
                    <button key={currentFolder} className="showBtn">{currentFolder}</button>
                    <div className="show-content" tabindex="-1">
                        {dropDown}
                    </div>
                </div>
                <button key="Next" className="toggleBtn" onClick={() => this.state.func(nextId)}>
                    <img alt=">" src={rightArrow}/>
                </button>
            </div>
        );
    }

    render()
    {
        const folders = this.state.folders;
        const currentId = this.state.currId;
        
        return(
            <div className="ShowBar">
                <a href={"/"}>
                    <button className="ButtonBack" onClick={this.BackToMenu}>
                        <img alt="Back" src={BackArrow}/>
                    </button>
                </a>
                <this.FolderBar currentId={currentId} folders={folders}/>
            </div>
        );
    }
}

export default ShowBar;