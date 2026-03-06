import axios from "axios"
import {useState} from "react"

function EncodePanel(){

const [file,setFile] = useState()
const [message,setMessage] = useState("")
const [key,setKey] = useState("")
const [result,setResult] = useState("")
const [mediaType,setMediaType] = useState("image")

const encode = async()=>{

if(mediaType !== "image"){
alert("This media type is not implemented yet")
return
}

let formData = new FormData()

formData.append("image",file)
formData.append("message",message)
formData.append("key",key)

const res = await axios.post(
"http://localhost:5000/encode-image",
formData
)

setResult(res.data.image)

}

return(

<div>

<h3>Encode Message</h3>

<br/>

<label>Cover Media Type</label>

<br/>

<select
value={mediaType}
onChange={(e)=>setMediaType(e.target.value)}
>

<option value="image">Image</option>
<option value="text">Text</option>
<option value="audio">Audio</option>
<option value="video">Video</option>

</select>

<br/><br/>

<label>Secret Message</label>

<br/>

<input
type="text"
placeholder="Enter secret message"
value={message}
onChange={(e)=>setMessage(e.target.value)}
/>

<br/><br/>

<label>Secret Key</label>

<br/>

<input
type="text"
placeholder="Enter secret key"
value={key}
onChange={(e)=>setKey(e.target.value)}
/>

<br/><br/>

<label>Upload Cover File</label>

<br/>

<input
type="file"
onChange={(e)=>setFile(e.target.files[0])}
/>

<br/><br/>

<button onClick={encode}>Encode</button>

<br/><br/>

{result && (

<div>

<h4>Encoded Image</h4>

<img src={result} width="300"/>

<br/><br/>

<a href={result} download="stego.png">
<button>Download Image</button>
</a>

</div>

)}

</div>

)

}

export default EncodePanel
