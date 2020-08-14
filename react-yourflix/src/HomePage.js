import React from 'react';
import Nav from './Nav/Nav';
import ProgramTable from './Programs/ProgramTable';

class HomePage extends React.Component
{
    render()
    {
        const testProg = "{\"0\":704,\"Id\":704,\"1\":10593,\"Folder_Id\":10593,\"2\":\"Avatar the Last Airbender\",\"Name\":\"Avatar the Last Airbender\"}";
        return(
            <div>
                <Nav/>
                <ProgramTable programs={testProg}/>
            </div>
        )
    }
}

export default HomePage