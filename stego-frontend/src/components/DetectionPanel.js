import axios from "axios"
import {useState} from "react"

function DetectionPanel(){

const [file,setFile] = useState()
const [prob,setProb] = useState()

const detect = async()=>{

let formData = new FormData()

formData.append("image",file)

const res = await axios.post("http://localhost:5000/detect",formData)

setProb(res.data.probability)

}

return(

<div>

<h3>AI Detection</h3>

<input type="file" onChange={(e)=>setFile(e.target.files[0])}/>

<button onClick={detect}>Detect</button>

<p>Probability: {prob}</p>

</div>

)

}

export default DetectionPanel