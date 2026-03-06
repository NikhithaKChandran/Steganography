import React,{useState} from "react"
import EncodePanel from "./components/EncodePanel"
import DecodePanel from "./components/DecodePanel"
import DetectionPanel from "./components/DetectionPanel"
import SmartCoverPanel from "./components/SmartCoverPanel"

function App(){

const [tab,setTab] = useState("encode")

return(

<div>

<h2>StegoShield</h2>

<button onClick={()=>setTab("encode")}>Encode</button>
<button onClick={()=>setTab("decode")}>Decode</button>
<button onClick={()=>setTab("detect")}>Detect</button>
<button onClick={()=>setTab("smart")}>Smart Cover</button>

{tab==="encode" && <EncodePanel/>}
{tab==="decode" && <DecodePanel/>}
{tab==="detect" && <DetectionPanel/>}
{tab==="smart" && <SmartCoverPanel/>}

</div>

)

}

export default App