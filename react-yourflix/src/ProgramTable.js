import React from 'react';
import Program from "./Program";
import './css/yf-program.css'
import testData from "./testdata.json"

class ProgramTable extends React.Component
{
    constructor(props)
    {
        super(props);

        this.state =
        {
            programs: testData
        };
        this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
        this.ShowPrograms = this.ShowPrograms.bind(this);
        this.screenWidth = React.createRef();
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
        this.setState(
            { 
                width: width
            });
    }

    GetNumCols(width)
    {
        if(width > 920)
            return 5;
        else if(width >= 640)
            return 4;
        else if(width > 360)
            return 3;
        else
            return 2;
    }

    ShowPrograms(props)
    {
        var returnPage = []
        var currentTable = []
        var currentRow = []
        var lastChar = ""
        var numTables = 0;
        var width = props.width;
        var padding = props.padding;
        var numCol = props.columns;
        var colIndex = 0;
        for(var i = 0; i < this.state.programs.length; i++)
        {
            var currentProg = JSON.parse(this.state.programs[i]);
            if(currentProg.Name.substring(0, 1) !== lastChar)
            {
                if(numTables > 0)
                {
                    currentTable.push(<tr>{currentRow}</tr>);
                    returnPage.push(
                    <table className="ProgramTable">
                        <thead>
                            <h1>{lastChar}</h1>
                        </thead>
                        <tbody>{currentTable}</tbody>
                    </table>);
                    currentTable = [];
                    currentRow = [];
                }
                numTables++;
                colIndex = 0;
                lastChar = currentProg.Name.substring(0, 1);
            }
            if(colIndex >= numCol)
            {
                currentTable.push(<tr>{currentRow}</tr>);
                colIndex = 0;
                currentRow = [];
            }

            currentRow.push(
            <th style={{minWidth:width, maxWidth:width, padding:padding/2}}>
                <Program width={width} program={currentProg}/>
            </th>
            );
            colIndex++;
        }
        return returnPage;
    }

    render()
    {
        var width = this.state.width ?? 0;
        const numCols = this.GetNumCols(width);
        var rowWidth = (width/this.GetNumCols(width));
        var rowPadding = 10;
        var colWidth = rowWidth - rowPadding;
        return(
            <div style={{width:"100%"}} ref={this.screenWidth}>
                <this.ShowPrograms columns={numCols} width={colWidth} padding={rowPadding}/>
            </div>
        );
    }
}

export default ProgramTable