import Guest from "./Guest"

function GuestsView(props) {
    var guests = [];
    props.guests.forEach(guest => {
        guests.push((<Guest title={guest.title} imageLink={guest.imageLink} videoLink={guest.videoLink} timelines={guest.timelines.join("<br/>")} />));
    });
    return (
        <div className="guestsView">
            {guests}
        </div>
    );
}


export default GuestsView;
