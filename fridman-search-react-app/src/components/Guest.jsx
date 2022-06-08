import "../styles/Guest.css"

function Guest(props) {
    return (
        <div className="guest">
            <img src={props.imageLink} className="podcastImage"/>
            <br/>
            <a className="guestTitle" href={props.videoLink}>{props.title}</a>
            <p dangerouslySetInnerHTML={{__html: props.timelines}} className="captions"></p>
            <br/>
        </div>
    );
}
export default Guest
