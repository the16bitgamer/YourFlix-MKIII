import React from 'react';
import ShowBar from './ShowBar';

class ShowPage extends React.Component
{
    render()
    {
        return(
            <div>
                <ShowBar name={"NAME_HERE"} folders={"JSON_FOLDER_HERE"}/>
            </div>
        );
    }
}

export default ShowPage;