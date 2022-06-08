import "../styles/SearchBar.css"
import React from "react"


function capitalize(word) {
    return word.charAt(0).toUpperCase() + word.slice(1)
}


function SearchBar(props) {
    const [state, setState] = React.useState({
        word: ""
    });

    function inputChanged(event) {
        var word = event.target.value;
        setState({
            ...state,
            word: capitalize(word) 
        });
    }

    async function searchForGuests() {
        const response = await fetch("http://localhost:8000/api/search?query={}".replace("{}", state.word.replace(" ", "%20")), 
                {mode: "cors"});
        if (response.status === 200) {
            const jsonData = await response.json();
            props.setParentState({guests: jsonData});
        }
    }

    async function handleKeyPress(e) {
        if (e.key === "Enter") {
            await searchForGuests();
        }
    }

    return (
        <div className="searchForm">
            <input type="search" placeholder="Phrase from podcast" value={state.word} className="searchBar" onChange={inputChanged} onKeyPress={handleKeyPress}/>
            <button className="searchButton" onClick={searchForGuests}>Search</button>
        </div>
    );
}


export default SearchBar;
