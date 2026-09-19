(function (root) {
    'use strict';

    if (!root || !root.document) {
        return;
    }

    var legacyQualificationCollector = root.GTB_SRWF_COLLECT_V1_QUALIFICATION_V034;
    var VERSION_MAP = Object.freeze({
        package: '0.3.6',
        structuralCollector: '0.3.0',
        admission: '0.3.2',
        v1QualificationCore: '0.3.4',
        radioCardGeometry: '0.3.5',
        visualRepairQualification: '0.3.6',
        finalQualificationComposer: '0.3.6'
    });

    function parkDiagnosticControls() {
        ['gtb-srwf-download-report', 'gtb-srwf-download-admission-report'].forEach(function (id) {
            var button = root.document.getElementById(id);
            if (!button || !button.style) {
                return;
            }
            button.style.position = 'static';
            button.style.left = 'auto';
            button.style.bottom = 'auto';
            button.style.zIndex = 'auto';
            button.style.display = 'inline-block';
            button.style.margin = '12px';
        });
    }

    function appendFailure(report, collector) {
        if (!report || typeof report !== 'object') {
            return;
        }
        if (!Array.isArray(report.collectorFailures)) {
            report.collectorFailures = [];
        }
        report.collectorFailures.push({ collector: collector, state: 'COLLECTOR_FAILED' });
    }

    function clearRepairEvidence(report) {
        if (!report || typeof report !== 'object') {
            return;
        }
        delete report.radioCardGeometry;
        delete report.binaryChoiceGeometry;
        delete report.visualRepairQualification;
        delete report.packageVersion;
        delete report.diagnosticVersionMap;
    }

    function collectRepairEvidence(report) {
        var radio = null;
        var visual = null;
        var failures = [];

        root.GTB_SRWF_RADIO_CARD_GEOMETRY_V035 = null;
        root.GTB_SRWF_VISUAL_REPAIR_QUALIFICATION_V035 = null;
        root.GTB_SRWF_VISUAL_REPAIR_QUALIFICATION_V036 = null;

        try {
            if (typeof root.GTB_SRWF_COLLECT_RADIO_CARD_GEOMETRY_V035 !== 'function') {
                throw new Error('radio card collector unavailable');
            }
            radio = root.GTB_SRWF_COLLECT_RADIO_CARD_GEOMETRY_V035();
            if (!radio || typeof radio !== 'object' || Array.isArray(radio)) {
                throw new Error('radio card collector returned invalid payload');
            }
        } catch (error) {
            radio = null;
            root.GTB_SRWF_RADIO_CARD_GEOMETRY_V035 = null;
            failures.push({ collector: 'radioCardGeometry', state: 'COLLECTOR_FAILED' });
            appendFailure(report, 'radioCardGeometry');
        }

        try {
            var visualCollector = root.GTB_SRWF_COLLECT_VISUAL_REPAIR_QUALIFICATION_V036 || root.GTB_SRWF_COLLECT_VISUAL_REPAIR_QUALIFICATION_V035;
            if (typeof visualCollector !== 'function') {
                throw new Error('visual repair collector unavailable');
            }
            visual = visualCollector();
            if (!visual || typeof visual !== 'object' || Array.isArray(visual)) {
                throw new Error('visual repair collector returned invalid payload');
            }
        } catch (error) {
            visual = null;
            root.GTB_SRWF_VISUAL_REPAIR_QUALIFICATION_V035 = null;
            root.GTB_SRWF_VISUAL_REPAIR_QUALIFICATION_V036 = null;
            failures.push({ collector: 'visualRepairQualification', state: 'COLLECTOR_FAILED' });
            appendFailure(report, 'visualRepairQualification');
        }

        return { radio: radio, visual: visual, failures: failures };
    }

    function collectComposedQualification() {
        var report = root.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03;
        clearRepairEvidence(report);

        if (typeof legacyQualificationCollector !== 'function') {
            throw new Error('v0.3.4 qualification core unavailable');
        }

        var qualification = legacyQualificationCollector();
        if (!qualification || typeof qualification !== 'object' || Array.isArray(qualification)) {
            throw new Error('v0.3.4 qualification core returned invalid payload');
        }

        var repair = collectRepairEvidence(report);
        qualification.packageVersion = VERSION_MAP.package;
        qualification.diagnosticVersionMap = VERSION_MAP;
        qualification.radioCardGeometry = repair.radio;
        qualification.visualRepairQualification = repair.visual;
        qualification.repairCollectorFailures = repair.failures;

        root.GTB_SRWF_V1_QUALIFICATION_V034 = qualification;
        root.GTB_SRWF_V1_QUALIFICATION_V035 = qualification;
        root.GTB_SRWF_V1_QUALIFICATION_V036 = qualification;

        if (report && typeof report === 'object') {
            report.packageVersion = VERSION_MAP.package;
            report.diagnosticVersionMap = VERSION_MAP;
            report.radioCardGeometry = repair.radio;
            report.binaryChoiceGeometry = repair.radio;
            report.visualRepairQualification = repair.visual;
            report.srwfV1Qualification = qualification;
        }

        return qualification;
    }

    parkDiagnosticControls();
    root.GTB_SRWF_DIAGNOSTIC_VERSION_MAP_V035 = VERSION_MAP;
    root.GTB_SRWF_DIAGNOSTIC_VERSION_MAP_V036 = VERSION_MAP;
    root.GTB_SRWF_COLLECT_V1_QUALIFICATION_V034 = collectComposedQualification;
    root.GTB_SRWF_COLLECT_V1_QUALIFICATION_V035 = collectComposedQualification;
    root.GTB_SRWF_COLLECT_V1_QUALIFICATION_V036 = collectComposedQualification;

    try {
        collectComposedQualification();
    } catch (error) {
        root.GTB_SRWF_V1_QUALIFICATION_V035 = null;
        root.GTB_SRWF_V1_QUALIFICATION_V036 = null;
    }
}(typeof window !== 'undefined' ? window : this));
