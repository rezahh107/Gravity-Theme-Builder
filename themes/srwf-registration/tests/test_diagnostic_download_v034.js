'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ASSETS = path.resolve(__dirname, '../diagnostic/assets');
const runtimeSource = fs.readFileSync(path.join(ASSETS, 'runtime-diagnostic.js'), 'utf8');
const qualificationSource = fs.readFileSync(path.join(ASSETS, 'srwf-v1-qualification.js'), 'utf8');
const provenanceSource = fs.readFileSync(path.join(ASSETS, 'version-provenance.js'), 'utf8');

function eventTargetElement(tagName) {
    const listeners = new Map();
    return {
        tagName: String(tagName || '').toUpperCase(),
        id: '',
        type: '',
        style: {},
        children: [],
        setAttribute() {},
        appendChild(node) { this.children.push(node); return node; },
        addEventListener(type, callback, options) {
            if (!listeners.has(type)) listeners.set(type, []);
            listeners.get(type).push({
                callback,
                capture: options === true || Boolean(options && options.capture)
            });
        },
        dispatchEvent(event) {
            const current = Object.assign({ target: this, currentTarget: this }, event || {});
            const entries = (listeners.get(current.type) || []).slice();
            entries.filter((entry) => entry.capture).forEach((entry) => entry.callback.call(this, current));
            entries.filter((entry) => !entry.capture).forEach((entry) => entry.callback.call(this, current));
            return true;
        },
        click() { return this.dispatchEvent({ type: 'click' }); }
    };
}

function makeBrowserHarness() {
    const nodesById = new Map();
    const downloads = [];
    let objectUrlCounter = 0;

    const body = {
        appendChild(node) {
            if (node && node.id) nodesById.set(node.id, node);
            return node;
        }
    };

    const documentObject = {
        readyState: 'complete',
        body,
        documentElement: body,
        activeElement: null,
        baseURI: 'https://example.test/registration/',
        styleSheets: [],
        addEventListener() {},
        getElementById(id) { return nodesById.get(id) || null; },
        createTextNode(text) { return { nodeType: 3, data: String(text) }; },
        createElement(tag) {
            if (tag === 'button') return eventTargetElement('button');
            if (tag === 'a') return { href: '', download: '', click() {} };
            return eventTargetElement(tag);
        },
        querySelectorAll() { return []; }
    };

    class FakeBlob {
        constructor(parts, options) {
            this.parts = parts;
            this.type = options && options.type ? options.type : '';
        }
    }

    const NativeURL = URL;
    class BrowserURL extends NativeURL {}
    BrowserURL.createObjectURL = (blob) => {
        downloads.push(JSON.parse(blob.parts.map(String).join('')));
        objectUrlCounter += 1;
        return 'blob:gtb-' + objectUrlCounter;
    };
    BrowserURL.revokeObjectURL = () => {};

    const contextObject = {
        console,
        document: documentObject,
        innerWidth: 640,
        Blob: FakeBlob,
        URL: BrowserURL,
        setTimeout(callback) { callback(); return 1; },
        clearTimeout() {},
        getComputedStyle() {
            return new Proxy({ getPropertyValue: () => '', getPropertyPriority: () => '' }, {
                get(target, property) { return property in target ? target[property] : ''; }
            });
        }
    };
    contextObject.window = contextObject;
    contextObject.globalThis = contextObject;

    const context = vm.createContext(contextObject);
    vm.runInContext(runtimeSource, context, { filename: 'runtime-diagnostic.js' });
    vm.runInContext(qualificationSource, context, { filename: 'srwf-v1-qualification.js' });

    context.GTB_SRWF_COLLECT_RADIO_CARD_GEOMETRY_V035 = () => ({ diagnosticVersion: '0.3.5', viewportCssWidth: context.innerWidth, fieldCount: 3 });
    context.GTB_SRWF_COLLECT_VISUAL_REPAIR_QUALIFICATION_V035 = () => ({ diagnosticVersion: '0.3.5', viewportCssWidth: context.innerWidth, targetCount: 1 });
    vm.runInContext(provenanceSource, context, { filename: 'version-provenance.js' });

    const button = documentObject.getElementById('gtb-srwf-download-report');
    assert.ok(button, 'diagnostic download control was not initialized');
    assert.strictEqual(typeof context.GTB_SRWF_COLLECT_V1_QUALIFICATION_V034, 'function', 'runtime-compatible final qualification callable missing');
    assert.strictEqual(typeof context.GTB_SRWF_COLLECT_V1_QUALIFICATION_V035, 'function', 'v0.3.5 composed qualification callable missing');
    assert.strictEqual(context.GTB_SRWF_V1_QUALIFICATION_V035.viewportCssWidth, 640, 'initial qualification fixture did not collect');

    return { context, button, downloads };
}

function latestDownload(harness) {
    assert.ok(harness.downloads.length > 0, 'download boundary was not reached');
    return harness.downloads[harness.downloads.length - 1];
}

function assertFreshQualification(report, expectedWidth, label) {
    assert.ok(report.srwfV1Qualification, label + ': qualification missing from downloaded report');
    assert.strictEqual(report.srwfV1Qualification.diagnosticVersion, '0.3.4', label + ': qualification core version changed');
    assert.strictEqual(report.srwfV1Qualification.viewportCssWidth, expectedWidth, label + ': downloaded qualification is stale');
    assert.strictEqual(report.packageVersion, '0.3.5', label + ': package version provenance missing');
    assert.strictEqual(report.diagnosticVersionMap.structuralCollector, '0.3.0', label + ': structural collector provenance missing');
    assert.strictEqual(report.diagnosticVersionMap.finalQualificationComposer, '0.3.5', label + ': composer provenance missing');
    assert.strictEqual(report.radioCardGeometry.viewportCssWidth, expectedWidth, label + ': radio geometry is stale');
    assert.strictEqual(report.visualRepairQualification.viewportCssWidth, expectedWidth, label + ': visual repair qualification is stale');
    assert.strictEqual(report.srwfV1Qualification.radioCardGeometry.viewportCssWidth, expectedWidth, label + ': composed radio evidence is stale');
    assert.strictEqual(report.srwfV1Qualification.visualRepairQualification.viewportCssWidth, expectedWidth, label + ': composed visual evidence is stale');
    assert.strictEqual(report.srwfV1Qualification.repairCollectorFailures.length, 0, label + ': unexpected repair collector failure');
    assert.strictEqual(
        Object.keys(report).filter((key) => key === 'srwfV1Qualification').length,
        1,
        label + ': qualification was attached more than once'
    );
}

const harness = makeBrowserHarness();

// Keyboard-style activation: a click can occur with no pointerdown.
harness.context.innerWidth = 700;
harness.button.dispatchEvent({ type: 'click', detail: 0 });
assertFreshQualification(latestDownload(harness), 700, 'keyboard click');

// Programmatic activation must use the same final assembly path.
harness.context.innerWidth = 760;
harness.button.click();
assertFreshQualification(latestDownload(harness), 760, 'programmatic click');

// Pointerdown remains an optional pre-capture optimization, never the freshness authority.
harness.context.innerWidth = 820;
harness.button.dispatchEvent({ type: 'pointerdown', pointerType: 'mouse' });
harness.context.innerWidth = 840;
harness.button.dispatchEvent({ type: 'click', detail: 1 });
assertFreshQualification(latestDownload(harness), 840, 'pointer activation');

// A repair collector failure must be visible and must not serialize stale success.
// Seed stale evidence explicitly: v0.3.5 intentionally does not rely on a long-lived global
// success snapshot, so this control proves the final composer clears even injected stale data.
harness.context.GTB_SRWF_VISUAL_REPAIR_QUALIFICATION_V035 = {
    diagnosticVersion: '0.3.5',
    viewportCssWidth: 840,
    targetCount: 1
};
harness.context.GTB_SRWF_COLLECT_VISUAL_REPAIR_QUALIFICATION_V035 = () => { throw new Error('forced visual repair failure'); };
harness.context.innerWidth = 880;
harness.button.dispatchEvent({ type: 'click', detail: 0 });
const repairFailedReport = latestDownload(harness);
assert.strictEqual(repairFailedReport.visualRepairQualification, null, 'stale visual repair evidence was serialized as current success');
assert.strictEqual(repairFailedReport.srwfV1Qualification.visualRepairQualification, null, 'stale nested visual repair evidence survived');
assert.ok(
    repairFailedReport.collectorFailures.some((item) => item.collector === 'visualRepairQualification' && item.state === 'COLLECTOR_FAILED'),
    'visual repair collector failure was not represented at the download boundary'
);
assert.ok(
    repairFailedReport.srwfV1Qualification.repairCollectorFailures.some((item) => item.collector === 'visualRepairQualification'),
    'visual repair collector failure was not represented in composed qualification evidence'
);

// Restore the repair collector before testing legacy qualification failure.
harness.context.GTB_SRWF_COLLECT_VISUAL_REPAIR_QUALIFICATION_V035 = () => ({ diagnosticVersion: '0.3.5', viewportCssWidth: harness.context.innerWidth, targetCount: 1 });

// A stale successful legacy qualification must not survive a fresh core failure at final assembly.
const staleQualification = harness.context.GTB_SRWF_V1_QUALIFICATION_V034;
harness.context.GTB_SRWF_COLLECT_V1_QUALIFICATION_V034 = () => { throw new Error('forced qualification failure'); };
harness.context.GTB_SRWF_V1_QUALIFICATION_V034 = staleQualification;
harness.context.innerWidth = 900;
harness.button.dispatchEvent({ type: 'click', detail: 0 });
const failedReport = latestDownload(harness);
assert.strictEqual(Object.prototype.hasOwnProperty.call(failedReport, 'srwfV1Qualification'), false, 'stale qualification was serialized as current success');
assert.ok(
    failedReport.collectorFailures.some((item) => item.collector === 'srwfV1Qualification' && item.state === 'COLLECTOR_FAILED'),
    'fresh qualification failure was not represented in bounded collector failure evidence'
);
assert.strictEqual(harness.context.GTB_SRWF_V1_QUALIFICATION_V034, null, 'failed final capture left stale core qualification marked current');

assert.strictEqual(harness.downloads.length, 5, 'unexpected number of diagnostic downloads');
console.log('PASS: final diagnostic download is activation-independent, version-explicit, fresh, and stale-repair-safe');
