/*
ref: https://makandracards.com/luis-romero/30231-mongodb-list-all-collections-by-size
mongo --port 27018 collection_name test.js
*/

var collectionNames = db.getCollectionNames(), stats = [];
collectionNames.forEach(function (n) { stats.push(db[n].stats()); });
stats = stats.sort(function(a, b) { return b['size'] - a['size']; });
for (var c in stats) { print(stats[c]['ns'] + ": " + stats[c]['size'] + " (" + stats[c]['storageSize'] + ")"); }
