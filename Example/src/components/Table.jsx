import React from "react";
import { JsonToTable } from "react-json-to-table";

function Table(props){
      return (
          <div>
              {/* Import library, inside props data for table.*/}
              <JsonToTable json={props.aboutlocation} />
          </div>
      )
}

export default Table;