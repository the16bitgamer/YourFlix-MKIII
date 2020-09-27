import React from 'react';
import ShowTile from './ShowTile';

class BuildShowTable extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state = 
        {
            showData: props.ShowData,
            width: 0,
            lastWidth: 1
        }

        this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
        this.screenWidth = React.createRef();
    }

    shouldComponentUpdate(nextProps) 
    {
        if(this.state.showData !== nextProps.ShowData)
        {     
            this.setState({ showData: nextProps.ShowData});
        }

        return true;
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
        var width = this.screenWidth.current.offsetWidth;
        console.log(width);
        this.GetNumCols(width);
        this.setState(
            { 
                width: width
            });
    }
    
    GetNumCols(width)
    {
        var currWidth = 0;
        if(width > 920)
            currWidth = 3;
        else if(width >= 640)
            currWidth = 2;
        else
            currWidth = 1;
        
        if(this.state.lastWidth !== currWidth)
        {
            this.setState(
            { 
                lastWidth: currWidth
            });
        }
        return currWidth;
    }

    BuildTable(props)
    {
        const content = props.Shows;
        const width = props.Width;
        const numRows = props.Row;
        const padding = props.Padding;

        var contentArray = [];
        var tableRowArray = [];
        var currIndex = 0;
        var row = 0;

        for(var i = 0; i < content.length; i++)
        {
            const currentContent = JSON.parse(content[i]);
            if(currIndex === numRows)
            {
                tableRowArray.push(
                    <tr key={"row-"+row}>
                        {contentArray}
                    </tr>
                );
                currIndex = 0;
                row++;
                contentArray = [];
            }
            currIndex++;
            contentArray.push(
                <th key={"element-"+currentContent.Content_Id} style={{minWidth:width, maxWidth:width, padding:padding/2}}>
                    <ShowTile Name={currentContent.Content_Name} Id={currentContent.Content_Id}/>
                </th>
            );
        }
        tableRowArray.push(
            <tr key={"row-"+row}>
                {contentArray}
            </tr>
        );
        return(
            <table className="ContentTable">
                <tbody>
                    {tableRowArray}
                </tbody>
            </table>
        );
    }

    render()
    {
        var showData = this.state.showData;
        
        var width = this.state.width ?? 360;
        const numCols = this.state.lastWidth;
        var rowWidth = (width/numCols);
        var rowPadding = 10;
        var colWidth = rowWidth - rowPadding;

        return(
            <div style={{width:"100%"}} ref={this.screenWidth}>
                <this.BuildTable Shows={showData} Width={colWidth} Row={numCols} Padding={rowPadding}/>
            </div>
        );
    }
}
export default BuildShowTable;