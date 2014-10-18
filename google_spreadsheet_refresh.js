function onOpen() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var menuEntries = [ {name: "Refresh This Sheet", functionName: "Refresh"},
                     {name: "Refresh All Sheets", functionName: "RefreshAll"}
                    ];
  ss.addMenu("Looker", menuEntries); 
}
function onInstall(e) {
  onOpen(e);
}



function Refresh(sheet){
  var ss = SpreadsheetApp.getActiveSheet();
  if (typeof(sheet) !== 'undefined'){
    ss = sheet;
  }
  var range = ss.getDataRange();
  var cells_of_imports = find("ImportXML",range);
  for (var i = 0;i<cells_of_imports.length;i++){
    cells_of_imports[i].setValue(cells_of_imports[i].getFormula().replace(/.html[^"]*"/, '.html?refresh='+new Date().getTime()+'"'));
  }
}

function RefreshAll(){
  var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
  for (var i = 0;i<sheets.length;i++){
    Refresh(sheets[i]);
  }
}


function find(value, range) {
  var data = range.getFormulas();
  var list = [];
  for (var i = 0; i < data.length; i++) {
    for (var j = 0; j < data[i].length; j++) {
      if (data[i][j].indexOf(value) > -1) {
        list.push(range.getCell(i + 1, j + 1));
      }
    }
  }
  return list;
}