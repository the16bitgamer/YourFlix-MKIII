import React from 'react';
import Program from "./Program";
import './css/yf-programTable.css';

class ProgramTable extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state =
        {
            programs: props.Programs,
            lastWidth: 1,
            sortByName: props.SortByName
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
            currWidth = 5;
        else if(width >= 640)
            currWidth = 4;
        else if(width > 360)
            currWidth = 3;
        else
            currWidth = 2;
        
        if(this.state.lastWidth !== currWidth)
        {
            this.setState(
            { 
                lastWidth: currWidth
            });
        }
        return currWidth;
    }
    
    ShowPrograms(props)
    {
        var returnPage = [];
        var currentTable = [];
        var currentRow = [];
        var tableHeadder = "";
        var numTables = 0;
        var width = props.width;
        var padding = props.padding;
        var numCol = props.columns;
        var sorting = this.state.sortByName;
        var colIndex = 0;
        var programs = this.state.programs;

        for(var i = 0; i < programs.length; i++)
        {
            var currentProg = JSON.parse(programs[i]);
            if(currentProg.Program_Name.substring(0, 1).toUpperCase() !== tableHeadder && sorting)
            {
                if(numTables > 0)
                {
                    currentTable.push(<tr key={"row-"+i}>{currentRow}</tr>);
                    returnPage.push(
                    <table key={"table-"+i} className="ProgramTable">
                        <thead key={"head-"+i}>
                            <h1 key={"Name-"+i}>{tableHeadder}</h1>
                        </thead>
                        <tbody key={"body-"+i}>{currentTable}</tbody>
                    </table>);
                    currentTable = [];
                    currentRow = [];
                }
                numTables++;
                colIndex = 0;
                tableHeadder = currentProg.Program_Name.substring(0, 1).toUpperCase();
            }
            if(colIndex >= numCol)
            {
                currentTable.push(<tr key={"row-"+i}>{currentRow}</tr>);
                colIndex = 0;
                currentRow = [];
            }
            var programLink = "/Show?id=" + currentProg.First_Folder;

            if(currentProg.Num_Content === 1)
            {
                programLink = "/Video?id=" + currentProg.First_Content;
            }

            currentRow.push(
            <th key={"element-"+i} style={{minWidth:width, maxWidth:width, padding:padding/2}}>
                <Program key={currentProg.Program_Id} width={width} program={currentProg} link={programLink}/>
            </th>
            );
            colIndex++;
        }

        currentTable.push(<tr key={"row-"+i}>{currentRow}</tr>);
        returnPage.push(
            <table key={"table-"+i} className="ProgramTable">
                <thead key={"head-"+i}>
                    <h1 key={"Name-"+i}>{tableHeadder}</h1>
                </thead>
                <tbody key={"body-"+i}>{currentTable}</tbody>
            </table>);

        return returnPage;
    }

    render()
    {
        var width = this.state.width ?? 360;
        const numCols = this.state.lastWidth;
        var rowWidth = (width/numCols);
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