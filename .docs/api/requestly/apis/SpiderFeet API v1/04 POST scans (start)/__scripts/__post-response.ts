pm.test('status 201', function () { pm.response.to.have.status(201); });
var j = pm.response.json();
pm.environment.set('scan_id', j.scan_id);
pm.test('has poll url', function () { pm.expect(j.poll).to.include(j.scan_id); });