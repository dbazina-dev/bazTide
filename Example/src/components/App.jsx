import React, {useState} from "react";
import Datepicker from "react-datepicker";
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import {format as fm} from "date-fns"
import Graph from "./Graph";
import Table from "./Table";
import SearchBox from "./Searchbox";
import "./containers.css";
import "react-datepicker/dist/react-datepicker.css";


function App(){

    const [location, setLocation]=useState("");                         //Used to store value of searchbox
    const [startDate, setStartDate]=useState(new Date());               //Used to store value of start date
    const [endDate, setEndDate]=useState(new Date());                   //Used to store value of end date
    const [graphData, setGraphData]=useState([]);                       //Used to store data for graph
    const [locationData, setLocationData]=useState([]);                 //Used to store data for location
    const [open, setOpen]=useState(false);                              //Used to verify should snackbar show or not
    const [responseSatus, setResponseStatus]=useState({
        isError:false,                                                  //Boolean for any error.
        locationError:false,                                            //Boolean for location error.
        locationMessage:'',                                             //Special message for location error
        message:"",                                                     //Message for snackbar
        networkError:false,                                             //Boolean for network error,server offline
        type:'info',                                                    //Standard for severity
    })
    function handleClick(event){
        var tideUrl=encodeURI(`http://127.0.0.1:5000/data/${location}/tidedata?start=${fm(startDate,'yyyy-MM-dd kk:mm')}&end=${fm(endDate,'yyyy-MM-dd kk:mm')}`)
        fetch(tideUrl).then((response)=> {
            if (response.ok){
                return response.json()
            } 
            else{
                response.json().then(data => {
                    throw new Error(data.message)
                  })
                .catch((error)=>{
                    setResponseStatus(oldState=> ({ ...oldState, shouldOpen:true, networkError: false, isError: true, message: error.message, type:'error'}))
                })                 
            }
        })
        .then((data) => {
            //Updates data to variable that is used for graph.
            setGraphData(data)
            //Updates status of response
            setResponseStatus(oldState => ({ ...oldState, shouldOpen:true, networkError: true, isError: false, message:'Data was fetched succesfuly!', type:'success'}));   
        })
        .catch((error) => {
            //Checks error message, return error if server is offline.
            setResponseStatus(oldState => ({ ...oldState, networkError: true, message:'Server is offline!', type:'warning'}));
        });
        //Second fetch request onclick, used for retrieving information about location.
        var locationUrl=encodeURI(`http://127.0.0.1:5000//data/${location}/metadata`)
        fetch(locationUrl)
        .then(function(response) {
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            return response;})
        .then(response => response.json())
        .then((data) => {
            //Updates status of response
            setResponseStatus(oldState => ({ ...oldState, networkError: false, locationError: false,}));
            //Updates data to variable that is used for table
            setLocationData(data)
        })
        .catch((error) => {
            if((error.message==="NetworkError when attempting to fetch resource.") || (error.message==="Failed to fetch")){
                //Checks error message, return error if server is offline.
                setResponseStatus(oldState => ({ ...oldState, networkError: true, message:'Server is offline!', type:'warning'}));
            }
            else{
                //Any other error.
                setResponseStatus(oldState => ({ ...oldState, locationError: true, locationMessage:"There are no details for provided location"}));
            }
        });
        setOpen(true)
        event.preventDefault() //Prevents page from loading, because of submit function.
    }
    //Function used for Snackbar, used for closing.
    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
          return;
        }   
        setOpen(false);
      };

    //Function used for Snackbar, imported library.
    function Alert(props) {
        return <MuiAlert elevation={6} variant="filled" {...props} />;
    }
    function handleChange(newValue) {           //Callback function
        setLocation(newValue);
      } 
    return(
        <div className="container">
            <h1 className="heading">BazTide</h1>
            {/* Snackbar component, used to inform user about status of request. */}
            <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
                <Alert onClose={handleClose} severity={responseSatus.type}>
                    {responseSatus.message}
                </Alert>
            </Snackbar>
            <div className="first-grid-container">
                <form onSubmit={handleClick}>
                    <div className="input-container">
                        <label>
                            {/* Searchbox component that send props, implementing callback!*/}
                            Set location: <SearchBox value={location} onChange={handleChange} />
                        </label>
                    </div>
                    <div className="input-container">
                        <div className="customDatePickerWidth">
                            {/* Datepicker for starting date */}
                            <label>
                                Set starting date:<Datepicker className="input-field" selected={startDate} onChange={date => setStartDate(date)} showTimeSelect dateFormat="yyyy-MM-dd HH:mm" required="reqired" />
                            </label>
                        </div>       
                    </div>
                    <div className="input-container">
                        <div className="customDatePickerWidth">
                            {/* Datepicker for end date */}
                            <label>
                                Set ending date:<Datepicker className="input-field" selected={endDate} onChange={date => setEndDate(date)} showTimeSelect dateFormat="yyyy-MM-dd HH:mm" required="reqired" />
                            </label>
                        </div> 
                    </div>
                    <div className="input-container">
                        <button className="submit-button" type="submit">Submit</button>
                    </div>
                </form>
                {/* Conditional rendering. If there is error with response, render div instead of component*/}
                { responseSatus.isError ? <p>Something is wrong!</p>:   
                <div className="graph-container">
                    <Graph somedata={graphData}/>
                </div>
                }
            </div>    
            <div className="grid-container">
                <div className="grid-child">
                    <h3 className="heading">Tide data</h3>
                    {/* Conditional rendering. If there is error with response, render div instead of component*/}
                    { responseSatus.isError ? <div>Something went wrong!</div>:
                    <Table aboutlocation={graphData}></Table>}
                </div>
                <div className="grid-child">
                    <h3 className="heading">Location data</h3>
                    {/* Conditional rendering. If there is error with response, render div instead of component*/}
                    { responseSatus.locationError ? <div>{responseSatus.locationMessage}</div>:
                    <Table aboutlocation={locationData}></Table>}
                </div>
            </div>
        </div>
    )
}
export default App;
