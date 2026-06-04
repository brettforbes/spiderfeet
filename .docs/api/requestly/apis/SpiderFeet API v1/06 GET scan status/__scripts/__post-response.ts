pm.test('status 200', function () { pm.response.to.have.status(200); });
pm.test('scan_id matches', function () {
  var j = pm.response.json();
  pm.expect(j.scan_id).to.eql(pm.environment.get('scan_id'));
});