(function (root, factory) {
    'use strict';

    var api = factory();

    if (typeof module === 'object' && module.exports) {
        module.exports = api;
    }

    function capture(documentObject) {
        var report = api.buildReport(root.GTB_SRWF_RUNTIME_ADMISSION_DECISIONS, documentObject);
        root.GTB_SRWF_RUNTIME_ADMISSION_DIAGNOSTIC_V032 = report;
        return report;
    }

    function startBrowser() {
        if (!root || !root.document) {
            return;
        }

        capture(root.document);
        var button = api.ensureDownloadControl(root.document);
        if (button && typeof button.addEventListener === 'function') {
            button.addEventListener('click', function () {
                api.downloadJson(root.document, root, capture(root.document));
            });
        }
    }

    if (root && root.document) {
        if (root.document.readyState === 'loading') {
            root.document.addEventListener('DOMContentLoaded', startBrowser, { once: true });
        } else {
            startBrowser();
        }
    }
}(typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : this), function () {
    'use strict';

    var SCHEMA_VERSION = 'v0.2';
    var DIAGNOSTIC_VERSION = '0.3.2';
    var DOWNLOAD_CONTROL_ID = 'gtb-srwf-download-admission-report';
    var PRODUCTION_STYLESHEET_ID = 'srwf-registration-theme-css';
    var MAX_DECISIONS = 8;
    var CONTEXTS = Object.freeze({ registration: true, gravity_flow_entry_detail: true, unknown: true });
    var EVIDENCE = Object.freeze({
        registration_default: true,
        gravity_flow_early_enqueue: true,
        gravity_flow_content_bracket: true,
        unknown: true
    });
    var REASONS = Object.freeze({
        unrelated_form: true,
        gravity_flow_entry_detail: true,
        production_admission_unavailable: true
    });

    function safeDecision(input) {
        input = input && typeof input === 'object' ? input : {};
        var context = typeof input.renderingContext === 'string' && CONTEXTS[input.renderingContext]
            ? input.renderingContext : 'unknown';
        var evidence = typeof input.contextEvidence === 'string' && EVIDENCE[input.contextEvidence]
            ? input.contextEvidence : 'unknown';
        var reason = input.exclusionReason === null
            ? null
            : (typeof input.exclusionReason === 'string' && REASONS[input.exclusionReason]
                ? input.exclusionReason : null);
        var admitted = input.presentationAdmitted === true
            ? true
            : (input.presentationAdmitted === false ? false : null);

        return {
            formIdentityMatched: input.formIdentityMatched === true,
            presentationAdmitted: admitted,
            renderingContext: context,
            contextEvidence: evidence,
            exclusionReason: reason
        };
    }

    function stylesheetPresent(documentObject) {
        return Boolean(
            documentObject &&
            typeof documentObject.getElementById === 'function' &&
            documentObject.getElementById(PRODUCTION_STYLESHEET_ID)
        );
    }

    function buildReport(decisions, documentObject) {
        var source = Array.isArray(decisions) ? decisions.slice(0, MAX_DECISIONS) : [];
        return {
            schemaVersion: SCHEMA_VERSION,
            diagnosticVersion: DIAGNOSTIC_VERSION,
            diagnosticMode: 'admin-gated-read-only-context-admission',
            admissionDecisions: source.map(safeDecision),
            srwfStylesheetPresent: stylesheetPresent(documentObject),
            truncated: Array.isArray(decisions) && decisions.length > MAX_DECISIONS
        };
    }

    function ensureDownloadControl(documentObject) {
        if (!documentObject || typeof documentObject.getElementById !== 'function') {
            return null;
        }

        var existing = documentObject.getElementById(DOWNLOAD_CONTROL_ID);
        if (existing) {
            return existing;
        }
        if (!documentObject.body || typeof documentObject.createElement !== 'function') {
            return null;
        }

        var button = documentObject.createElement('button');
        button.id = DOWNLOAD_CONTROL_ID;
        button.type = 'button';
        button.setAttribute('aria-label', 'دانلود تصمیم زمینه نمایش GTB');
        button.style.position = 'fixed';
        button.style.left = '16px';
        button.style.bottom = '68px';
        button.style.zIndex = '2147483647';
        button.style.padding = '10px 14px';
        button.style.cursor = 'pointer';
        if (typeof documentObject.createTextNode === 'function' && typeof button.appendChild === 'function') {
            button.appendChild(documentObject.createTextNode('دانلود تصمیم GTB'));
        }
        documentObject.body.appendChild(button);
        return button;
    }

    function downloadJson(documentObject, view, report) {
        if (!documentObject || !view || typeof view.Blob !== 'function' || !view.URL || typeof view.URL.createObjectURL !== 'function') {
            return false;
        }
        var anchor = documentObject.createElement('a');
        var blob = new view.Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
        var url = view.URL.createObjectURL(blob);
        anchor.href = url;
        anchor.download = 'gtb-srwf-admission-diagnostic-v0.3.2.json';
        if (documentObject.body && typeof documentObject.body.appendChild === 'function') {
            documentObject.body.appendChild(anchor);
        }
        if (typeof anchor.click === 'function') {
            anchor.click();
        }
        if (typeof anchor.remove === 'function') {
            anchor.remove();
        }
        if (typeof view.URL.revokeObjectURL === 'function') {
            view.URL.revokeObjectURL(url);
        }
        return true;
    }

    return {
        SCHEMA_VERSION: SCHEMA_VERSION,
        DIAGNOSTIC_VERSION: DIAGNOSTIC_VERSION,
        MAX_DECISIONS: MAX_DECISIONS,
        safeDecision: safeDecision,
        stylesheetPresent: stylesheetPresent,
        buildReport: buildReport,
        ensureDownloadControl: ensureDownloadControl,
        downloadJson: downloadJson
    };
}));
