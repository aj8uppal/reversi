import { useState, useEffect } from "react";
import axios from "axios";

import Square from './Square.jsx';

import './Board.css';

const Board = () => {
    const WIDTH = 8;
    const HEIGHT = 8;
    const WHITE = 1;
    const BLACK = 2;
    let starting_board = [...Array(WIDTH)].map(e => Array(HEIGHT).fill(0));
    starting_board[WIDTH / 2 - 1][HEIGHT / 2 - 1] = 1;
    starting_board[WIDTH / 2][HEIGHT / 2] = 1;
    starting_board[WIDTH / 2 - 1][HEIGHT / 2] = 2;
    starting_board[WIDTH / 2][WIDTH / 2 - 1] = 2;

    const [board, setBoard] = useState(starting_board);
    const [useAi, setUseAi] = useState(true);
    const [id, setId] = useState(0);
    const [whiteState, setWhiteState] = useState(); // 1: white, 2: black
    const [blackState, setBlackState] = useState(); // 1: white, 2: black
    const [currentPlayer, setCurrentPlayer] = useState(WHITE);

    const move = (x, y, use_ai, color, to_flip) => {
        let current_color = color || currentPlayer;
        let current_state = (current_color === WHITE ? whiteState : blackState);
        if(!id || board[x][y] || Object.keys(current_state).indexOf(x+","+y) === -1){
            return;
        }
        console.log("here");
        let copy = [...board];
        copy[x][y] = current_color;
        let flips = to_flip || current_state[x+","+y];
        // debugger;
        let offset = 0;
        while(true){
            let bunch = [];
            for(let dir in flips){
                if(flips[dir].length > offset){
                    bunch.push(flips[dir][offset]);
                }
            }
            if(bunch.length){
                setTimeout( () => {
                    let copy = [...board];
                    console.log(bunch);
                    for(let i = 0; i < bunch.length; i++){
                        copy[bunch[i][0]][bunch[i][1]] = current_color;
                    }
                    setBoard(copy);
                }, 200 + offset*200);
                offset+=1;
            }else{
                break;
            }
        }
        // for(let dir in flips){
        //     for(let p = 0; p < flips[dir].length; p++){
        //         let piece = flips[dir][p]
        //         copy[piece[0]][piece[1]] = current_color;
        //     }
        // }
        // setBoard(copy);
        setCurrentPlayer(3 - current_color);
        if(use_ai){
            // let opponent = 3 - current_color;
            setTimeout( () => {
                // setCurrentPlayer(3 - opponent);
                get_ai_move(x, y)
            }, 500+offset*200);
        }
    }

    const get_ai_move = async (x, y) => {
        const res = await axios.post("/move", {move: [x, y], id: id, use_ai: true, color: currentPlayer});
        move(...res.data.move, false, BLACK, res.data.flips);
        setWhiteState(res.data.states[WHITE]);
        setBlackState(res.data.states[BLACK]);
    }
    
    useEffect( () => {
        const startGame = async () => {
            const res = await axios.post("/new_game");
            if(res && res.data && res.data.id){
                setId(res.data.id);
                setWhiteState(res.data.states[WHITE]);
                setBlackState(res.data.states[BLACK]);
            }
        }
        startGame();
    }, [])

    return <div className={`board ${currentPlayer === WHITE ? "white" : "black"}-to-move`}>
        {whiteState && blackState && board.map((col, y) => {
            return col.map((item, x) => {
                let valid = board[y][x] || y+","+x in (currentPlayer === 1 ? whiteState : blackState);
                return <Square move={() => move(y, x, useAi)} value={item} className={`${valid ? "valid" : "invalid"}`}/>
            })
        })}
    </div>
}

export default Board;