import axios from "axios"
import {useState} from "react"

function SmartCoverPanel(){

const [file,setFile] = useState()
const [capacity,setCapacity] = useState()
const [score,setScore] = useState()

const analyze = async()=>{

let formData = new FormData()

formData.append("image",file)

const res = await axios.post("http://localhost:5000/smart-select",formData)

setCapacity(res.data.capacity)
setScore(res.data.score)

}

return(

<div>

<h3>Smart Image Selection</h3>

<input type="file" onChange={(e)=>setFile(e.target.files[0])}/>

<button onClick={analyze}>Analyze</button>

<p>Capacity: {capacity}</p>
<p>Security Score: {score}</p>

</div>

)

}

export default SmartCoverPanel