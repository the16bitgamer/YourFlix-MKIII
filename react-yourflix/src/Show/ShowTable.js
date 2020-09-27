import React from 'react';
import BuildShowTable from './BuildShowTable';
import Fetch from '../Database/Fetch';

class ShowTable extends React.Component
{
    constructor(props)
    {
        super(props);
        const currentId = props.currentId;
        this.state = 
        {
            currId: currentId,
            showData: [],
            pulled: false
        }

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
        Fetch("/php/GetFolderContent.php", this.ContentReturn, requestOptions);
    }

    ContentReturn(results)
    {
        this.setState(
            {
                showData: results,
                pulled: true
            });
    }

    shouldComponentUpdate(nextProps) 
    {
        if(this.state.currId !== nextProps.currentId)
        {     
            this.PullContent(nextProps.currentId);
            this.setState({ currId: nextProps.currentId});
        }

        return true;
    }

    render()
    {
        var pulled = this.state.pulled;
        if(pulled)
        {
            var showData = this.state.showData;
            return(
                <BuildShowTable ShowData={showData}/>
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

export default ShowTable;