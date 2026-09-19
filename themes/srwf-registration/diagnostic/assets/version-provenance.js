(function (root) {
    'use strict';

    if (!root || !root.document) {
        return;
    }

    var VERSION_MAP = Object.freeze({
        package: '0.3.5',
        structuralCollector: '0.3.0',
        admission: '0.3.2',
        radioCardGeometry: '0.3.5',
        v1Qualification: '0.3.5',
        provenanceAugmenter: '0.3.5'
    });

    function augment() {
        var report = root.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03;
        if (!report || typeof report !== 'object') {
            return null;
        }
        report.packageVersion = VERSION_MAP.package;
        report.diagnosticVersionMap = VERSION_MAP;
        if (root.GTB_SRWF_RADIO_CARD_GEOMETRY_V035) {
            report.radioCardGeometry = root.GTB_SRWF_RADIO_CARD_GEOMETRY_V035;
            report.binaryChoiceGeometry = root.GTB_SRWF_RADIO_CARD_GEOMETRY_V035;
        }
        if (root.GTB_SRWF_V1_QUALIFICATION_V035) {
            report.srwfV1Qualification = root.GTB_SRWF_V1_QUALIFICATION_V035;
        }
        return report;
    }

    var button = root.document.getElementById('gtb-srwf-download-report');
    augment();
    if (button && typeof button.addEventListener === 'function') {
        button.addEventListener('pointerdown', augment);
        button.addEventListener('click', augment, true);
    }
}(typeof window !== 'undefined' ? window : this));
