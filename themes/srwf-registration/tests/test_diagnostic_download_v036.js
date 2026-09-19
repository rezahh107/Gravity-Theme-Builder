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
        tagName: String(tagName || '').toUpperCase(), id: '', type: '', style: {}, children: [],
        setAttribute() {},
        appendChild(node) { this.children.push(node); return node; },
        addEventListener(type, callback, options) {
            if (!listeners.has(type)) listeners.set(type, []);
            listeners.get(type).push({ callback, capture: options === true || Boolean(options && options.capture) });
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

const nodesById = new Map();
const downloads = [];
const body = { appendChild(node) { if (node && node.id) nodesById.set(node.id, node); return node; } };
const documentObject = {
    readyState: 'complete', body, documentElement: body, activeElement: null,
    baseURI: 'https://example.test/registration/', styleSheets: [],
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
    constructor(parts, options) { this.parts = parts; this.type = options && options.type ? options.type : ''; }
}
class BrowserURL extends URL {}
BrowserURL.createObjectURL = (blob) => {
    downloads.push(JSON.parse(blob.parts.map(String).join('')));
    return 'blob:gtb-' + downloads.length;
};
BrowserURL.revokeObjectURL = () => {};

const contextObject = {
    console, document: documentObject, innerWidth: 390, devicePixelRatio: 3,
    Blob: FakeBlob, URL: BrowserURL,
    setTimeout(callback) { callback(); return 1; }, clearTimeout() {},
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

context.GTB_SRWF_COLLECT_RADIO_CARD_GEOMETRY_V035 = () => ({
    diagnosticVersion: '0.3.5', viewportCssWidth: context.innerWidth, fieldCount: 3
});
context.GTB_SRWF_COLLECT_VISUAL_REPAIR_QUALIFICATION_V036 = () => ({
    diagnosticVersion: '0.3.6', viewportCssWidth: context.innerWidth,
    devicePixelRatio: context.devicePixelRatio,
    targetCount: 1,
    targets: [{ widthChain: { wrapper: { rect: { width: context.innerWidth - 32 } } } }]
});
vm.runInContext(provenanceSource, context, { filename: 'version-provenance.js' });

const button = documentObject.getElementById('gtb-srwf-download-report');
assert.ok(button, 'diagnostic download control was not initialized');
assert.strictEqual(typeof context.GTB_SRWF_COLLECT_V1_QUALIFICATION_V036, 'function');

context.innerWidth = 393;
context.devicePixelRatio = 2.75;
button.dispatchEvent({ type: 'click', detail: 0 });
assert.strictEqual(downloads.length, 1);
let report = downloads[0];
assert.strictEqual(report.packageVersion, '0.3.6');
assert.strictEqual(report.diagnosticVersionMap.visualRepairQualification, '0.3.6');
assert.strictEqual(report.visualRepairQualification.viewportCssWidth, 393);
assert.strictEqual(report.visualRepairQualification.devicePixelRatio, 2.75);
assert.strictEqual(report.visualRepairQualification.targets[0].widthChain.wrapper.rect.width, 361);
assert.strictEqual(report.srwfV1Qualification.visualRepairQualification.viewportCssWidth, 393);

context.innerWidth = 430;
context.devicePixelRatio = 3;
button.click();
assert.strictEqual(downloads.length, 2);
report = downloads[1];
assert.strictEqual(report.visualRepairQualification.viewportCssWidth, 430, 'download serialized stale viewport evidence');
assert.strictEqual(report.visualRepairQualification.devicePixelRatio, 3, 'download serialized stale DPR evidence');
assert.strictEqual(report.visualRepairQualification.targets[0].widthChain.wrapper.rect.width, 398);

console.log('PASS: diagnostic 0.3.6 download composes fresh viewport, DPR, and width-chain evidence at activation time');
