// SELECT ELEMENTS

const testDiv = document.getElementById('api-test')

// CREATE ELEMENTS

// api url
const api_url = 'https://hymnary.org/api/scripture?reference=Psalm+136';

// EVENT LISTENERS



// FUNCTIONS

async function getData(url){
    // e.preventDefault();
    
    const response = await fetch(url);
    let data = await response.json();
    console.log(data);
}
// Calling that async function
getData(api_url);

// Function to define innerHTML for HTML table
