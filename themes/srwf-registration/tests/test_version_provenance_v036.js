'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const source = fs.readFileSync(path.join(__dirname, '../diagnostic/assets/version-provenance.js'), 'utf8');
let legacyCalls = 0;
let radioCalls = 0;
let visualCalls = 0;

function button() {
    return { style: { position: 'fixed', left: '12px', bottom: '12px', zIndex: '999' } };
}
const controls = {
    'gtb-srwf-download-report': button(),
    'gtb-srwf-download-admission-report': button()
};

const windowObject = {
    document: {
        readyState: 'complete',
        addEventListener() { throw new Error('complete-state composer must not defer control parking'); },
        getElementById(id) { return controls[id] || null; }
    },
    GTB_SRWF_RUNTIME_DIAGNOSTIC_V03: { diagnosticVersion: '0.3.0', collectorFailures: [] },
    GTB_SRWF_COLLECT_V1_QUALIFICATION_V034() {
        legacyCalls += 1;
        return { diagnosticVersion: '0.3.4', source: 'qualification-core' };
    },
    GTB_SRWF_COLLECT_RADIO_CARD_GEOMETRY_V035() {
        radioCalls += 1;
        return { diagnosticVersion: '0.3.5', fieldCount: 6 };
    },
    GTB_SRWF_COLLECT_VISUAL_REPAIR_QUALIFICATION_V036() {
        visualCalls += 1;
        return { diagnosticVersion: '0.3.6', targetCount: 1, viewportCssWidth: 393, devicePixelRatio: 3 };
    }
};

vm.runInNewContext(source, { window: windowObject, console }, { filename: 'version-provenance.js' });

assert.strictEqual(legacyCalls, 1);
assert.strictEqual(radioCalls, 1);
assert.strictEqual(visualCalls, 1);
assert.deepStrictEqual(
    JSON.parse(JSON.stringify(windowObject.GTB_SRWF_DIAGNOSTIC_VERSION_MAP_V036)),
    {
        package: '0.3.6',
        structuralCollector: '0.3.0',
        admission: '0.3.2',
        v1QualificationCore: '0.3.4',
        radioCardGeometry: '0.3.5',
        visualRepairQualification: '0.3.6',
        finalQualificationComposer: '0.3.6'
    }
);
assert.deepStrictEqual(
    JSON.parse(JSON.stringify(windowObject.GTB_SRWF_DIAGNOSTIC_VERSION_MAP_V035)),
    JSON.parse(JSON.stringify(windowObject.GTB_SRWF_DIAGNOSTIC_VERSION_MAP_V036)),
    'legacy alias must point to current package provenance'
);

Object.values(controls).forEach((control) => {
    assert.strictEqual(control.style.position, 'static');
    assert.strictEqual(control.style.left, 'auto');
    assert.strictEqual(control.style.bottom, 'auto');
    assert.strictEqual(control.style.zIndex, 'auto');
    assert.strictEqual(control.style.display, 'inline-block');
    assert.strictEqual(control.style.margin, '12px');
});

const fresh = windowObject.GTB_SRWF_COLLECT_V1_QUALIFICATION_V036();
assert.strictEqual(legacyCalls, 2);
assert.strictEqual(radioCalls, 2);
assert.strictEqual(visualCalls, 2);
assert.strictEqual(fresh.packageVersion, '0.3.6');
assert.strictEqual(fresh.radioCardGeometry.fieldCount, 6);
assert.strictEqual(fresh.visualRepairQualification.viewportCssWidth, 393);
assert.strictEqual(fresh.visualRepairQualification.devicePixelRatio, 3);
assert.deepStrictEqual(JSON.parse(JSON.stringify(fresh.repairCollectorFailures)), []);
assert.strictEqual(windowObject.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03.packageVersion, '0.3.6');

windowObject.GTB_SRWF_COLLECT_RADIO_CARD_GEOMETRY_V035 = () => { throw new Error('fixture failure'); };
const degraded = windowObject.GTB_SRWF_COLLECT_V1_QUALIFICATION_V036();
assert.strictEqual(degraded.radioCardGeometry, null);
assert.strictEqual(degraded.visualRepairQualification.targetCount, 1);
assert.deepStrictEqual(
    JSON.parse(JSON.stringify(degraded.repairCollectorFailures)),
    [{ collector: 'radioCardGeometry', state: 'COLLECTOR_FAILED' }]
);
assert.ok(windowObject.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03.collectorFailures.some((item) => item.collector === 'radioCardGeometry'));

console.log('PASS: v0.3.6 provenance composes fresh width evidence, preserves compatibility aliases, fails closed, and immediately parks already-created diagnostic controls when DOM readiness is complete');
