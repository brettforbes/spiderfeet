pm.test('status 200', function () { pm.response.to.have.status(200); });
pm.test('results array', function () { pm.expect(pm.response.json()).to.be.an('array'); });