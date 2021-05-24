import React, {useState, useEffect} from "react";

function SearchBox(props) {

    const [chars, setChars]=useState("");             //Chars from input
    const [result, setResult]=useState([]);           //Result after filtering
    const [loading, setLoading] = useState(true);     //For loading
    const [okay, setOkay] = useState(false);          //Boolean for status of server

    useEffect(() => {
        if (chars.length >= 1) {                      
          var locationListUrl=encodeURI(`http://127.0.0.1:5000/search/${chars}`) //Encode url
          fetch(locationListUrl)
          .then(function(response) {
            if (!response.ok) {                       //If response is not okay, throw error.
              throw new Error(response.status);
            }
            return response;})
          .then((res) => res.json())
          .then((data) => {
            setResult(data)                           //Using hooks to append data to variable.
            setLoading(false)
            setOkay(false)
          })
          .catch((error) => {
            if((error.message==="NetworkError when attempting to fetch resource.") || (error.message==="Failed to fetch")){
              setOkay(true)                           //Server error.
            }
            console.log(error)
          });
        }
      },[chars]);

    const handleChange = (e) => {                     //Handle change of input
        e.preventDefault()
        setChars(e.currentTarget.value.toLowerCase());
    };
    const handleSecondChange = (e) => {               //Handle change of select, callback on app.
      props.onChange(e.currentTarget.value)
  };

    return(
        <div>      
            <div>
              <input type="text" onChange={(e) => handleChange(e)} required="required" placeholder="Type..."/>
            </div>
            <div style={{marginTop:"15px"}}>
              {/* Conditional render, if server is offline, return message. */}
              {okay?<p>Server is offline!</p>:
              <select disabled={loading} required="required" value={props.location} onChange={(e) => handleSecondChange(e)} className="input-field">
              <option value="">Choose here</option>
              {/* Map results of filtering. */}
              {result.map(item => (
                  <option key={item.Name} value={item.Name}>{item.Name}</option>))}
              </select>}
            </div>
        </div>
    )
}

export default SearchBox;
