'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const source = fs.readFileSync(path.join(__dirname, '../diagnostic/assets/version-provenance.js'), 'utf8');
let legacyCalls = 0;
let radioCalls = 0;
let visualCalls = 0;

const windowObject = {
    document: {},
    GTB_SRWF_RUNTIME_DIAGNOSTIC_V03: { diagnosticVersion: '0.3.0', collectorFailures: [] },
    GTB_SRWF_COLLECT_V1_QUALIFICATION_V034() {
        legacyCalls += 1;
        return { diagnosticVersion: '0.3.4', source: 'qualification-core' };
    },
    GTB_SRWF_COLLECT_RADIO_CARD_GEOMETRY_V035() {
        radioCalls += 1;
        return { diagnosticVersion: '0.3.5', fieldCount: 6 };
    },
    GTB_SRWF_COLLECT_VISUAL_REPAIR_QUALIFICATION_V035() {
        visualCalls += 1;
        return { diagnosticVersion: '0.3.5', targetCount: 1 };
    }
};

vm.runInNewContext(source, { window: windowObject, console }, { filename: 'version-provenance.js' });

assert.strictEqual(legacyCalls, 1, 'composer should perform an initial fresh qualification composition');
assert.strictEqual(radioCalls, 1);
assert.strictEqual(visualCalls, 1);
assert.deepStrictEqual(
    JSON.parse(JSON.stringify(windowObject.GTB_SRWF_DIAGNOSTIC_VERSION_MAP_V035)),
    {
        package: '0.3.5',
        structuralCollector: '0.3.0',
        admission: '0.3.2',
        v1QualificationCore: '0.3.4',
        radioCardGeometry: '0.3.5',
        visualRepairQualification: '0.3.5',
        finalQualificationComposer: '0.3.5'
    }
);

const fresh = windowObject.GTB_SRWF_COLLECT_V1_QUALIFICATION_V035();
assert.strictEqual(legacyCalls, 2, 'download-time composer must re-run the v0.3.4 core');
assert.strictEqual(radioCalls, 2, 'download-time composer must re-measure radio geometry');
assert.strictEqual(visualCalls, 2, 'download-time composer must re-measure visual repair consumers');
assert.strictEqual(fresh.packageVersion, '0.3.5');
assert.strictEqual(fresh.radioCardGeometry.fieldCount, 6);
assert.strictEqual(fresh.visualRepairQualification.targetCount, 1);
assert.deepStrictEqual(JSON.parse(JSON.stringify(fresh.repairCollectorFailures)), []);
assert.strictEqual(windowObject.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03.packageVersion, '0.3.5');
assert.strictEqual(windowObject.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03.radioCardGeometry.fieldCount, 6);
assert.strictEqual(windowObject.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03.visualRepairQualification.targetCount, 1);

windowObject.GTB_SRWF_COLLECT_RADIO_CARD_GEOMETRY_V035 = () => { throw new Error('fixture failure'); };
const degraded = windowObject.GTB_SRWF_COLLECT_V1_QUALIFICATION_V035();
assert.strictEqual(degraded.radioCardGeometry, null, 'failed fresh collector must not retain stale radio evidence');
assert.strictEqual(degraded.visualRepairQualification.targetCount, 1, 'independent fresh collector should still be retained');
assert.deepStrictEqual(
    JSON.parse(JSON.stringify(degraded.repairCollectorFailures)),
    [{ collector: 'radioCardGeometry', state: 'COLLECTOR_FAILED' }]
);
assert.ok(windowObject.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03.collectorFailures.some((item) => item.collector === 'radioCardGeometry'));

console.log('PASS: v0.3.5 provenance composer exposes module versions, refreshes evidence at composition time, and fails closed without stale repair evidence');
