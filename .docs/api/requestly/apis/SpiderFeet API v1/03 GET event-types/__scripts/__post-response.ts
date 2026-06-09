pm.test('status 200', function () { pm.response.to.have.status(200); });
pm.test('has INTERNET_NAME', function () {
  var list = pm.response.json();
  pm.expect(list.some(function (t) { return t.name === 'INTERNET_NAME'; })).to.be.true;
});