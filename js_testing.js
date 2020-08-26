// this is wrapped in an `async` function
// you can use await throughout the function
var inputData = {sq_itm: "blah,blah", sq_qty: "1,1"};

var itemList1 = inputData.sq_itm.split(',');
var qtyList1 = inputData.sq_qty.split(',');
var bag_taken = 0;

for (var i = 0; i < itemList1.length; i++) {
  if (itemList1[i] = "blah") {
    bag_taken = bag_taken + valueOf(qtyList1[i]);
  }
};
console.log(qtyList1[i]);

console.log(bag_taken);
