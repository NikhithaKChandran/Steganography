import axios from "axios"
import { useState } from "react"

function DecodePanel(){

const [file,setFile] = useState(null)
const [message,setMessage] = useState("")
const [key,setKey] = useState("")

const decode = async()=>{

if(!file){
alert("Please upload a stego file")
return
}

if(!key){
alert("Please enter the secret key")
return
}

let formData = new FormData()

formData.append("image",file)
formData.append("key",key)

try{

const res = await axios.post(
"http://localhost:5000/decode-image",
formData,
{
headers:{
"Content-Type":"multipart/form-data"
}
}
)

setMessage(res.data.message)

}catch(err){

console.log(err)
alert("Decoding failed")

}

}

const downloadMessage = () => {

if(!message){
alert("No message to download")
return
}

const element = document.createElement("a")
const file = new Blob([message], {type:"text/plain"})
element.href = URL.createObjectURL(file)
element.download = "decoded_message.txt"
document.body.appendChild(element)
element.click()

}

return(

<div>

<h3>Decode Message</h3>

<br/>

<label>Upload Stego File</label>

<br/>

<input
type="file"
onChange={(e)=>setFile(e.target.files[0])}
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

<button onClick={decode}>
Decode
</button>

<br/><br/>

<h4>Decoded Message</h4>

<div style={{
border:"1px solid gray",
padding:"10px",
minHeight:"40px",
width:"300px"
}}>

{message ? message : "No message extracted yet"}

</div>

<br/>

<button onClick={downloadMessage}>
Download Message
</button>

</div>

)

}

export default DecodePanel
