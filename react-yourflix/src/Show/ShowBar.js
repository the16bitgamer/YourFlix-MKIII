import React from 'react';

function ShowBar(props)
{
    const progName = props.Name;
    const folders = props.Folders;
    return(
        <table>
            <tbody>
                <tr>
                    <th>{progName}</th>
                    <th>{folders /* Add Season Bar here */}</th>
                </tr>
            </tbody>
        </table>
    );
}

export default ShowBar;