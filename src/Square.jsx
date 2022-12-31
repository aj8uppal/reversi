import './Square.css';

const Square = (props) => {
    const handleClick = (e) => {
        props.move();
    }
    return <div className={`square ${props.className}`} onClick={handleClick}>
                <div className={`marker ${props.value === 0 ? "blank" : props.value === 1 ? "white" : "black"}`}>

                </div>
            </div>
}

export default Square;