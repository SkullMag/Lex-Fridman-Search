import './styles/App.css';
import SearchBar from "./components/SearchBar"
import GuestsView from "./components/GuestsView"
import React from "react"
import logo from "./assets/lexfridman.jpg"


function App() {
    const [state, setState] = React.useState({
        guests: [] 
    });
    return (
        <div className="App">
            <img src={logo} className="logo" />
            <h1 className="title">Lex Fridman Search</h1>
            <SearchBar setParentState={setState}/>
            <GuestsView guests={state.guests}/>
            <p className="author">Created by <a href="https://instagram.com/rybalko._.oleg">Oleg Rybalko</a></p>
        </div>
    );
}


export default App;
