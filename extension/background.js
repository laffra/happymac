chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  updateTab(tab);
});

chrome.tabs.onActivated.addListener(function(activeInfo) {
  chrome.tabs.get(activeInfo.tabId, function (tab) {
    updateTab(tab);
  });
});

function updateTab(tab) {
  var port_number = 1187;
  while (port_number < 1287) {
    try {
      var url = "http://localhost:" + port_number + "/happymac?" +
        "url=" + encodeURIComponent(tab.url) + "&" +
        "fav=" + encodeURIComponent(tab.favIconUrl) + "&" +
        "title=" + encodeURIComponent(tab.title);
      var xhr = new XMLHttpRequest();
      xhr.open('GET', url);
      xhr.send();
      break;
    } catch (e) {
      console.log(e);
    }
    port_number++;
      break;
  }
}