// this is wrapped in an `async` function
// you can use await throughout the function
var inputData = {sq_itm: "blah,blah,blow,blah", sq_qty: "1,1,2,3"};

var itemList1 = inputData.sq_itm.split(',');
var qtyList1 = inputData.sq_qty.split(',').map(x=>+x);
var bag_taken = 0;
var n = qtyList1[0] + qtyList1[1];

for (var i = 0; i < itemList1.length; i++) {
  if (itemList1[i] = "blah") {
    bag_taken = bag_taken + valueOf(qtyList1[i]);
  }
  console.log(bag_taken);
};

var bags = new Object();
  bags.qty = bag_taken;
console.log(bags);

console.log(n);
console.log(itemList1);
console.log(qtyList1);
