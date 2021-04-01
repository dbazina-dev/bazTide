import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import moment from "moment";

function Graph(props){
    return (
      <AreaChart
      width={1200}
      height={450}
      data={props.somedata}
      margin={{
        top: 0, right: 30, left: 50, bottom: 15,
      }}>
        {/* Imported library from recharts. Inside props data for graph */}
        <CartesianGrid strokeDasharray="3 3" />
        {/* Formated string from props as date object, and remove excess. */}
        <XAxis dataKey="Time" tickFormatter={timeStr => moment(timeStr,'hh:mm').format('hh:mm')}/>
        <YAxis dataKey="Height" />
        <Tooltip/>
        <Legend />
        {/* Data on graph*/}
        <Area type="monotone" dataKey="Height" stroke="#8884d8" fill="#8884d8" />
        <Area type="monotone" dataKey="Tide" stroke="#8b0000"/>
        <Area type="monotone" dataKey="Date" stroke="#006400"/>
      </AreaChart>
    )
}
export default Graph;