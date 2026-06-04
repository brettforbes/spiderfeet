pm.test('status 200', function () { pm.response.to.have.status(200); });
pm.test('ok', function () {
  var j = pm.response.json();
  pm.expect(j.status).to.eql('ok');
  pm.expect(j.service).to.eql('spiderfeet-api');
});