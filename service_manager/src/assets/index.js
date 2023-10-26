import React from 'react'
import ReactDOM from 'react-dom'
import App from "../App";

const root = document.getElementById('js-framework-home')

ReactDOM.render(<App/>, root)

// const App = () => {
//     const [count, setCount] = React.useState(0)
//     const onClick = () => setCount(c => c + 1)
//     return (
//         <div>
//             <h1>The count is {count}</h1>
//             <button onClick={onClick}>Count</button>
//         </div>
//     )
// }

