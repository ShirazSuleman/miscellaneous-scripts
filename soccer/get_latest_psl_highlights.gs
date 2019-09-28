function getNewVideos() {
  var playlistId = "UUZH6G3Z5XINU6r92QN1l5Lw";
  var numHoursPrevious = 96;
  
  var d = new Date();
  d.setHours(d.getHours() - numHoursPrevious);
  var fromDate = d.toISOString();
  
  clearSpreadsheet();
  
  var results = getYoutubeVideos(fromDate, playlistId);
  
  writeToSpreadsheet(results);
}

function clearSpreadsheet() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var rangeList  = sheet.getRangeList(['A2:B10000']);
  rangeList.clearContent();
}

function writeToSpreadsheet(results) {
  var rowNum = 2;
  for (var i = 0; i < results.length; i++) {
    if (results[i].snippet.title.indexOf("Absa Premiership") > -1 && results[i].snippet.title.indexOf("Highlights") > -1){
      var url = "https://www.youtube.com/video/" + results[i].snippet.resourceId.videoId;
      var title = results[i].snippet.title
      Logger.log(url);
      Logger.log(title);
      SpreadsheetApp.getActiveSheet().getRange('A' + rowNum).setValue(title);
      SpreadsheetApp.getActiveSheet().getRange('B' + rowNum).setValue(url);
      rowNum += 1;
    }
  }
}

function getYoutubeVideos(fromDate, playlistId) {
  var results = [];
  var nextPageToken = null;
  
  do {
    var data = YouTube.PlaylistItems.list('snippet', { maxResults: 50, playlistId: playlistId, pageToken: nextPageToken });
    
    for (var i = 0; i < data.items.length; i++) {
      if (data.items[i].snippet.publishedAt > fromDate) {
        results.push(data.items[i]);
      }
    }
    
    nextPageToken = data.nextPageToken;
  }
  while (data.items[data.items.length - 1].snippet.publishedAt > fromDate)
  
  return results;
}
