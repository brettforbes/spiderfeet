pm.test('status 200', function () { pm.response.to.have.status(200); });
pm.test('has sfp_dnsresolve', function () {
  var list = pm.response.json();
  pm.expect(list.some(function (m) { return m.name === 'sfp_dnsresolve'; })).to.be.true;
});