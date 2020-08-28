import fetch from "isomorphic-fetch";

function Fetch(pullLocation, returnFunction, requestOptions)
{

    if(!requestOptions)
    {
        requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        };
    }    
    
    fetch(pullLocation, requestOptions)
    .then(response => response.json())
    .then(data => {
        returnFunction(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

export default Fetch;