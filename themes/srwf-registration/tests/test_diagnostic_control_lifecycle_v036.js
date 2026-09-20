'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ASSETS = path.resolve(__dirname, '../diagnostic/assets');
const sources = [
    'runtime-diagnostic.js',
    'binary-choice-geometry.js',
    'admission-diagnostic.js',
    'srwf-v1-qualification.js',
    'visual-repair-qualification.js',
    'version-provenance.js'
].map((name) => [name, fs.readFileSync(path.join(ASSETS, name), 'utf8')]);

function eventTargetElement(tagName) {
    const listeners = new Map();
    return {
        tagName: String(tagName || '').toUpperCase(),
        id: '',
        type: '',
        style: {},
        children: [],
        classList: [],
        setAttribute() {},
        appendChild(node) { this.children.push(node); return node; },
        addEventListener(type, callback, options) {
            if (!listeners.has(type)) listeners.set(type, []);
            listeners.get(type).push({
                callback,
                capture: options === true || Boolean(options && options.capture),
                once: Boolean(options && options.once)
            });
        },
        dispatchEvent(event) {
            const current = Object.assign({ target: this, currentTarget: this }, event || {});
            const entries = (listeners.get(current.type) || []).slice();
            const ordered = entries.filter((entry) => entry.capture).concat(entries.filter((entry) => !entry.capture));
            ordered.forEach((entry) => entry.callback.call(this, current));
            if (entries.some((entry) => entry.once)) {
                listeners.set(current.type, (listeners.get(current.type) || []).filter((entry) => !entry.once));
            }
            return true;
        },
        click() { return this.dispatchEvent({ type: 'click', detail: 0 }); },
        remove() {}
    };
}

const nodesById = new Map();
const documentListeners = new Map();
const deferredTasks = [];
const blobPayloads = [];
const anchorDownloads = [];

const body = eventTargetElement('body');
body.appendChild = function appendChild(node) {
    this.children.push(node);
    if (node && node.id) nodesById.set(node.id, node);
    return node;
};
body.contains = () => false;

const documentObject = {
    readyState: 'loading',
    body,
    documentElement: body,
    activeElement: null,
    baseURI: 'https://example.test/registration/',
    styleSheets: [],
    addEventListener(type, callback, options) {
        if (!documentListeners.has(type)) documentListeners.set(type, []);
        documentListeners.get(type).push({ callback, once: Boolean(options && options.once) });
    },
    getElementById(id) { return nodesById.get(id) || null; },
    createTextNode(text) { return { nodeType: 3, data: String(text) }; },
    createElement(tag) {
        if (String(tag).toLowerCase() === 'a') {
            const anchor = eventTargetElement('a');
            anchor.href = '';
            anchor.download = '';
            anchor.click = function click() {
                anchorDownloads.push({ href: this.href, download: this.download });
                return true;
            };
            return anchor;
        }
        return eventTargetElement(tag);
    },
    querySelectorAll() { return []; }
};

function fireDOMContentLoaded() {
    documentObject.readyState = 'interactive';
    const entries = (documentListeners.get('DOMContentLoaded') || []).slice();
    entries.forEach((entry) => entry.callback.call(documentObject, { type: 'DOMContentLoaded', target: documentObject }));
    documentListeners.set('DOMContentLoaded', (documentListeners.get('DOMContentLoaded') || []).filter((entry) => !entry.once));
}

function runDeferredTasks() {
    while (deferredTasks.length) {
        deferredTasks.shift()();
    }
}

class FakeBlob {
    constructor(parts, options) {
        this.parts = parts;
        this.type = options && options.type ? options.type : '';
    }
}
class BrowserURL extends URL {}
BrowserURL.createObjectURL = (blob) => {
    blobPayloads.push(JSON.parse(blob.parts.map(String).join('')));
    return 'blob:gtb-' + blobPayloads.length;
};
BrowserURL.revokeObjectURL = () => {};

const contextObject = {
    console,
    document: documentObject,
    innerWidth: 390,
    devicePixelRatio: 3,
    Blob: FakeBlob,
    URL: BrowserURL,
    GTB_SRWF_RUNTIME_ADMISSION_DECISIONS: [{
        formIdentityMatched: true,
        presentationAdmitted: true,
        renderingContext: 'registration',
        contextEvidence: 'registration_default',
        exclusionReason: null
    }],
    setTimeout(callback) { deferredTasks.push(callback); return deferredTasks.length; },
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

sources.forEach(([name, source]) => {
    vm.runInContext(source, context, { filename: name });
});

assert.strictEqual(documentObject.readyState, 'loading');
assert.strictEqual(documentObject.getElementById('gtb-srwf-download-report'), null,
    'fixture must not pre-create the runtime-report control');
assert.strictEqual(documentObject.getElementById('gtb-srwf-download-admission-report'), null,
    'fixture must not pre-create the admission-report control');
assert.strictEqual(blobPayloads.length, 0);
assert.strictEqual(anchorDownloads.length, 0);

fireDOMContentLoaded();

const runtimeButton = documentObject.getElementById('gtb-srwf-download-report');
const admissionButton = documentObject.getElementById('gtb-srwf-download-admission-report');
assert.ok(runtimeButton, 'runtime diagnostic producer did not create its control on DOMContentLoaded');
assert.ok(admissionButton, 'admission diagnostic producer did not create its control on DOMContentLoaded');
assert.strictEqual(runtimeButton.style.position, 'fixed',
    'producer control should still have its original fixed style before the deferred composer pass');
assert.strictEqual(admissionButton.style.position, 'fixed',
    'producer control should still have its original fixed style before the deferred composer pass');
assert.ok(deferredTasks.length > 0, 'composer did not schedule a post-DOMContentLoaded settlement pass');

runDeferredTasks();

[runtimeButton, admissionButton].forEach((control) => {
    assert.strictEqual(control.style.position, 'static');
    assert.strictEqual(control.style.left, 'auto');
    assert.strictEqual(control.style.bottom, 'auto');
    assert.strictEqual(control.style.zIndex, 'auto');
    assert.strictEqual(control.style.display, 'inline-block');
    assert.strictEqual(control.style.margin, '12px');
});

assert.strictEqual(typeof context.GTB_SRWF_COLLECT_V1_QUALIFICATION_V034, 'function');
assert.strictEqual(context.GTB_SRWF_COLLECT_V1_QUALIFICATION_V034, context.GTB_SRWF_COLLECT_V1_QUALIFICATION_V036,
    'final composer must remain the v0.3.6 activation boundary after deferred legacy collector installation');

context.innerWidth = 412;
context.devicePixelRatio = 2.625;
runtimeButton.click();
assert.strictEqual(blobPayloads.length, 1, 'runtime diagnostic download did not serialize a report');
assert.strictEqual(anchorDownloads.length, 1, 'runtime diagnostic download anchor was not activated');
assert.strictEqual(anchorDownloads[0].download, 'gtb-srwf-runtime-diagnostic-v0.3.0.json');
const runtimeReport = blobPayloads[0];
assert.strictEqual(runtimeReport.packageVersion, '0.3.6');
assert.strictEqual(runtimeReport.diagnosticVersionMap.finalQualificationComposer, '0.3.6');
assert.strictEqual(runtimeReport.visualRepairQualification.viewportCssWidth, 412,
    'runtime download did not compose fresh viewport evidence at activation time');
assert.strictEqual(runtimeReport.visualRepairQualification.devicePixelRatio, 2.625,
    'runtime download did not compose fresh DPR evidence at activation time');
assert.strictEqual(runtimeReport.srwfV1Qualification.visualRepairQualification.viewportCssWidth, 412);

admissionButton.click();
assert.strictEqual(blobPayloads.length, 2, 'admission diagnostic download did not serialize a report');
assert.strictEqual(anchorDownloads.length, 2, 'admission diagnostic download anchor was not activated');
assert.strictEqual(anchorDownloads[1].download, 'gtb-srwf-admission-diagnostic-v0.3.2.json');
const admissionReport = blobPayloads[1];
assert.strictEqual(admissionReport.diagnosticVersion, '0.3.2');
assert.strictEqual(admissionReport.admissionDecisions.length, 1);
assert.strictEqual(admissionReport.admissionDecisions[0].renderingContext, 'registration');

console.log('PASS: loading lifecycle creates both producer controls, defers final composer settlement, parks both overlays, preserves both downloads, and composes fresh v0.3.6 evidence at activation');
