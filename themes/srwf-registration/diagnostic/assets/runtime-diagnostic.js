(function (root, factory) {
    'use strict';

    var api = factory();

    if (typeof module === 'object' && module.exports) {
        module.exports = api;
    }

    function startBrowser() {
        if (!root || !root.document) {
            return;
        }

        var documentObject = root.document;
        var button = api.ensureDownloadControl(documentObject, root);
        var pendingResult = null;

        function capture() {
            pendingResult = api.run(documentObject, root);
            root.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03 = pendingResult;
            return pendingResult;
        }

        if (button && typeof button.addEventListener === 'function') {
            button.addEventListener('pointerdown', function () {
                try {
                    capture();
                } catch (error) {
                    pendingResult = null;
                }
            });

            button.addEventListener('click', function () {
                var result;
                try {
                    result = pendingResult || capture();
                    result = api.finalizeQualification(root, result);
                    root.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03 = result;
                    api.downloadJson(documentObject, root, result);
                } catch (error) {
                    root.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03 = {
                        schemaVersion: api.SCHEMA_VERSION,
                        diagnosticVersion: api.DIAGNOSTIC_VERSION,
                        diagnosticMode: 'admin-gated-read-only',
                        collectorFailures: [{ collector: 'report', state: 'COLLECTOR_FAILED' }]
                    };
                } finally {
                    pendingResult = null;
                }
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

    var SCHEMA_VERSION = 'v0.3';
    var DIAGNOSTIC_VERSION = '0.3.0';
    var TARGET_SELECTOR = '.gform-theme--framework.srwf-registration-theme_wrapper';
    var DOWNLOAD_CONTROL_ID = 'gtb-srwf-download-report';
    var BUDGETS = Object.freeze({
        targets: 4,
        normalControls: 64,
        submitControls: 8,
        validationNodes: 32,
        enhancedSelectSources: 12,
        tomSelectAssociationsPerSource: 4,
        uploadRoots: 16,
        uploadShallowNodesPerRoot: 24,
        gpfupRoots: 8,
        gpfupDropareasPerRoot: 4,
        fieldSignatures: 80,
        fieldShallowChildren: 8,
        stylesheetLinks: 128,
        titleConsumers: 8,
        sectionConsumers: 24,
        submitAncestorDepth: 8,
        cssRuleVisits: 4000,
        matchedCascadeRules: 96,
        conditionalContexts: 96,
        groupingContextDepth: 24,
        unrelatedForms: 8
    });

    var STYLE_PROPERTIES = [
        'display', 'position', 'width', 'height', 'inlineSize', 'minWidth', 'maxWidth',
        'minHeight', 'maxHeight', 'minInlineSize', 'maxInlineSize', 'minBlockSize', 'maxBlockSize',
        'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
        'marginTop', 'marginRight', 'marginBottom', 'marginLeft',
        'borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth',
        'borderTopStyle', 'borderRightStyle', 'borderBottomStyle', 'borderLeftStyle',
        'borderTopColor', 'borderRightColor', 'borderBottomColor', 'borderLeftColor',
        'borderRadius', 'backgroundColor', 'color', 'fontFamily', 'fontSize',
        'fontWeight', 'lineHeight', 'direction', 'boxSizing', 'zIndex',
        'visibility', 'opacity', 'flex', 'flexBasis', 'flexGrow', 'flexShrink',
        'justifyContent', 'alignItems', 'alignSelf', 'justifySelf',
        'gridTemplateColumns', 'gridColumn', 'gridColumnStart', 'gridColumnEnd'
    ];

    var CANONICAL_PROPERTIES = [
        '--gf-font-family-base',
        '--gf-color-primary',
        '--gf-color-danger',
        '--gf-color-success',
        '--gf-ctrl-bg-color',
        '--gf-ctrl-color',
        '--gf-ctrl-border-color',
        '--gf-ctrl-border-color-focus',
        '--gf-ctrl-border-color-error',
        '--gf-ctrl-radius',
        '--gf-ctrl-size',
        '--gf-ctrl-font-size',
        '--gf-ctrl-font-weight',
        '--gf-ctrl-label-color-primary',
        '--gf-ctrl-label-font-size-primary',
        '--gf-ctrl-label-font-weight-primary',
        '--gf-ctrl-desc-color',
        '--gf-ctrl-desc-color-error',
        '--gf-ctrl-btn-bg-color-primary',
        '--gf-ctrl-btn-bg-color-hover-primary',
        '--gf-ctrl-btn-bg-color-focus-primary',
        '--gf-ctrl-btn-color-primary',
        '--gf-ctrl-btn-radius',
        '--gf-ctrl-btn-size',
        '--gf-ctrl-btn-font-size',
        '--gf-ctrl-btn-font-weight',
        '--gf-ctrl-file-zone-radius',
        '--gf-field-section-border-color',
        '--gf-form-validation-heading-color'
    ];

    var SUBMIT_CASCADE_PROPERTIES = [
        'display', 'width', 'inline-size', 'min-width', 'min-inline-size',
        'max-width', 'max-inline-size', 'flex', 'flex-basis', 'flex-grow',
        'flex-shrink', 'align-self', 'justify-self'
    ];

    var SUBMIT_LOCAL_PROPERTIES = [
        '--gf-local-display', '--gf-local-width', '--gf-local-min-width', '--gf-local-max-width'
    ];

    var SAFE_ID_PATTERNS = [
        /^gform_wrapper_\d+$/,
        /^gform_\d+$/,
        /^gform_submit_button_\d+$/,
        /^field_\d+_\d+$/,
        /^input_\d+_\d+(?:_\d+)?$/,
        /^gform_multifile_upload_\d+_\d+$/
    ];

    function bounded(items, limit) {
        return Array.prototype.slice.call(items || [], 0, limit);
    }

    function safeClasses(element) {
        return bounded(element && element.classList ? element.classList : [], 48).map(String);
    }

    function safeStructuralId(element) {
        var id = element && typeof element.id === 'string' ? element.id : '';
        for (var i = 0; i < SAFE_ID_PATTERNS.length; i += 1) {
            if (SAFE_ID_PATTERNS[i].test(id)) {
                return id;
            }
        }
        return null;
    }

    function safeStateAttributes(element) {
        var result = {};
        var names = [
            'role', 'type', 'dir', 'aria-invalid', 'aria-expanded',
            'aria-hidden', 'aria-disabled', 'data-form-index'
        ];
        for (var i = 0; i < names.length; i += 1) {
            var name = names[i];
            if (element && typeof element.hasAttribute === 'function' && element.hasAttribute(name)) {
                result[name] = String(element.getAttribute(name));
            }
        }
        if (element) {
            result.multiple = Boolean(element.multiple);
            result.disabled = Boolean(element.disabled);
            result.required = Boolean(element.required);
        }
        return result;
    }

    function safeRect(element) {
        if (!element || typeof element.getBoundingClientRect !== 'function') {
            return null;
        }
        var rect = element.getBoundingClientRect();
        return {
            x: Number(rect.x || 0),
            y: Number(rect.y || 0),
            width: Number(rect.width || 0),
            height: Number(rect.height || 0)
        };
    }

    function computedPresentation(element, view) {
        if (!element || !view || typeof view.getComputedStyle !== 'function') {
            return {};
        }
        var style = view.getComputedStyle(element);
        var result = {};
        for (var i = 0; i < STYLE_PROPERTIES.length; i += 1) {
            var property = STYLE_PROPERTIES[i];
            result[property] = String(style[property] || '');
        }
        return result;
    }

    function fixedCustomProperties(element, view, properties) {
        if (!element || !view || typeof view.getComputedStyle !== 'function') {
            return {};
        }
        var style = view.getComputedStyle(element);
        var result = {};
        for (var i = 0; i < properties.length; i += 1) {
            var property = properties[i];
            result[property] = String(style.getPropertyValue(property) || '').trim();
        }
        return result;
    }

    function canonicalProperties(element, view) {
        return fixedCustomProperties(element, view, CANONICAL_PROPERTIES);
    }

    function elementSnapshot(element, view) {
        var rect = safeRect(element);
        var presentation = computedPresentation(element, view);
        var visible = Boolean(
            rect && rect.width > 0 && rect.height > 0 &&
            presentation.display !== 'none' && presentation.visibility !== 'hidden' && presentation.opacity !== '0'
        );
        return {
            tag: element && element.tagName ? String(element.tagName).toLowerCase() : '',
            structuralId: safeStructuralId(element),
            classes: safeClasses(element),
            state: safeStateAttributes(element),
            rect: rect,
            visible: visible,
            computed: presentation
        };
    }

    function selectSnapshot(select, view) {
        var snapshot = elementSnapshot(select, view);
        snapshot.optionCount = select && select.options ? Number(select.options.length || 0) : 0;
        snapshot.mode = select && select.multiple ? 'multiple' : 'single';
        snapshot.tomSelectEvidence = safeClasses(select).filter(function (name) {
            return name === 'tomselected' || name === 'ts-hidden-accessible';
        });
        return snapshot;
    }

    function boundedQuery(root, selector, limit) {
        if (!root || typeof root.querySelectorAll !== 'function') {
            return [];
        }
        return bounded(root.querySelectorAll(selector), limit);
    }

    function safeUrlMetadata(raw, base) {
        var result = { path: '', version: null };
        try {
            var parsed = new URL(String(raw || ''), String(base || 'http://invalid.local/'));
            result.path = parsed.pathname;
            var version = parsed.searchParams.get('ver');
            if (version && /^[0-9A-Za-z._-]{1,32}$/.test(version)) {
                result.version = version;
            }
        } catch (error) {
            result.path = '';
        }
        return result;
    }

    function collectStylesheetOrder(documentObject) {
        return boundedQuery(documentObject, 'link[rel="stylesheet"]', BUDGETS.stylesheetLinks).map(function (link, index) {
            var url = safeUrlMetadata(link && link.href, documentObject && documentObject.baseURI);
            var id = safeStructuralId(link);
            if (!id && link && typeof link.id === 'string' && /^(?:gravity|gform|srwf|gpp)[-_]/i.test(link.id)) {
                id = link.id;
            }
            return {
                index: index,
                id: id,
                path: url.path,
                version: id === 'srwf-registration-theme-css' ? url.version : null,
                media: link && typeof link.media === 'string' ? link.media : ''
            };
        });
    }

    function collectNormalControls(target, view) {
        return boundedQuery(target, 'input, select, textarea, button', BUDGETS.normalControls).map(function (element) {
            if (element && String(element.tagName || '').toLowerCase() === 'select') {
                return selectSnapshot(element, view);
            }
            return elementSnapshot(element, view);
        });
    }

    function collectSubmitControls(target, view) {
        return boundedQuery(target, 'button[type="submit"].gform_button, input[type="submit"].gform_button', BUDGETS.submitControls).map(function (element) {
            return elementSnapshot(element, view);
        });
    }

    function collectValidation(target, documentObject, view) {
        var states = boundedQuery(target, '.gform_validation_errors, .gfield_error, [aria-invalid="true"]', BUDGETS.validationNodes).map(function (element) {
            return elementSnapshot(element, view);
        });
        var focus = null;
        var active = documentObject ? documentObject.activeElement : null;
        if (active && target && typeof target.contains === 'function' && target.contains(active)) {
            focus = elementSnapshot(active, view);
        }
        return { states: states, focusOwner: focus };
    }

    function directChildrenWithClass(parent, className, limit) {
        if (!parent || !parent.children) {
            return [];
        }
        return bounded(parent.children, limit).filter(function (child) {
            return child && child.classList && typeof child.classList.contains === 'function' && child.classList.contains(className);
        });
    }

    function discoverTomSelect(source) {
        var found = [];
        function add(element, method) {
            if (!element || found.some(function (item) { return item.element === element; })) {
                return;
            }
            found.push({ element: element, method: method });
        }
        if (source && source.tomselect && source.tomselect.wrapper) {
            add(source.tomselect.wrapper, 'source.tomselect.wrapper');
        }
        if (source && source.nextElementSibling && source.nextElementSibling.classList && source.nextElementSibling.classList.contains('ts-wrapper')) {
            add(source.nextElementSibling, 'next-sibling.ts-wrapper');
        }
        directChildrenWithClass(source ? source.parentElement : null, 'ts-wrapper', 16).forEach(function (element) {
            add(element, 'parent-child.ts-wrapper');
        });
        if (source && typeof source.closest === 'function') {
            var field = source.closest('.gfield');
            var fieldMatches = boundedQuery(field, '.ts-wrapper', BUDGETS.tomSelectAssociationsPerSource);
            if (fieldMatches.length === 1) {
                add(fieldMatches[0], 'single-field.ts-wrapper');
            }
        }
        return bounded(found, BUDGETS.tomSelectAssociationsPerSource);
    }

    function collectEnhancedSelects(target, view) {
        return boundedQuery(target, 'select.tomselected, select.ts-hidden-accessible', BUDGETS.enhancedSelectSources).map(function (source) {
            var associations = discoverTomSelect(source).map(function (association) {
                var wrapper = association.element;
                return {
                    associationMethod: association.method,
                    wrapper: elementSnapshot(wrapper, view),
                    controls: boundedQuery(wrapper, '.ts-control', 2).map(function (element) { return elementSnapshot(element, view); }),
                    dropdowns: boundedQuery(wrapper, '.ts-dropdown', 2).map(function (element) { return elementSnapshot(element, view); })
                };
            });
            return { source: selectSnapshot(source, view), associations: associations };
        });
    }

    function shallowStructure(root, maxNodes) {
        var result = [];
        var queue = [{ element: root, depth: 0 }];
        while (queue.length && result.length < maxNodes) {
            var current = queue.shift();
            var element = current.element;
            if (!element) {
                continue;
            }
            var tag = String(element.tagName || '').toLowerCase();
            if (tag !== 'option') {
                result.push({
                    depth: current.depth,
                    tag: tag,
                    structuralId: safeStructuralId(element),
                    classes: safeClasses(element),
                    state: safeStateAttributes(element)
                });
            }
            if (current.depth >= 2 || tag === 'select' || !element.children) {
                continue;
            }
            bounded(element.children, maxNodes - result.length).forEach(function (child) {
                if (String(child.tagName || '').toLowerCase() !== 'option') {
                    queue.push({ element: child, depth: current.depth + 1 });
                }
            });
        }
        return result;
    }

    function collectUploads(target, view) {
        return boundedQuery(target, '.gform_fileupload_multifile, .ginput_container_fileupload, .gform_drop_area', BUDGETS.uploadRoots).map(function (uploadRoot) {
            return {
                root: elementSnapshot(uploadRoot, view),
                shallowStructure: shallowStructure(uploadRoot, BUDGETS.uploadShallowNodesPerRoot)
            };
        });
    }

    function collectGpfup(target, view) {
        var roots = boundedQuery(target, '.gpfup', BUDGETS.gpfupRoots).map(function (gpfupRoot) {
            return {
                root: elementSnapshot(gpfupRoot, view),
                strictMode: Boolean(gpfupRoot.classList && gpfupRoot.classList.contains('gpfup--strict')),
                dropareas: boundedQuery(gpfupRoot, '.gpfup__droparea', BUDGETS.gpfupDropareasPerRoot).map(function (droparea) {
                    return elementSnapshot(droparea, view);
                })
            };
        });
        return { state: roots.length ? 'RUNTIME_PROVEN' : 'NOT_OBSERVED', roots: roots };
    }

    function collectFieldSignatures(target) {
        return boundedQuery(target, '.gfield', BUDGETS.fieldSignatures).map(function (field) {
            return {
                structuralId: safeStructuralId(field),
                classes: safeClasses(field),
                children: bounded(field.children || [], BUDGETS.fieldShallowChildren).map(function (child) {
                    return { tag: String(child.tagName || '').toLowerCase(), structuralId: safeStructuralId(child), classes: safeClasses(child) };
                })
            };
        });
    }

    function splitSelectorList(selectorList) {
        var parts = [], start = 0, paren = 0, bracket = 0, quote = '', escaped = false;
        for (var i = 0; i < selectorList.length; i += 1) {
            var char = selectorList.charAt(i);
            if (escaped) { escaped = false; continue; }
            if (char === '\\') { escaped = true; continue; }
            if (quote) { if (char === quote) { quote = ''; } continue; }
            if (char === '"' || char === "'") { quote = char; continue; }
            if (char === '(') { paren += 1; continue; }
            if (char === ')') { paren -= 1; continue; }
            if (char === '[') { bracket += 1; continue; }
            if (char === ']') { bracket -= 1; continue; }
            if (char === ',' && paren === 0 && bracket === 0) {
                parts.push(selectorList.slice(start, i).trim()); start = i + 1;
            }
        }
        parts.push(selectorList.slice(start).trim());
        return parts.filter(Boolean);
    }

    function stylesheetMeta(sheet, index, documentObject) {
        var owner = sheet && sheet.ownerNode ? sheet.ownerNode : null;
        var url = safeUrlMetadata(owner && owner.href, documentObject && documentObject.baseURI);
        return {
            index: index,
            id: owner && typeof owner.id === 'string' && /^(?:gravity|gform|srwf|gpp)[-_]/i.test(owner.id) ? owner.id : null,
            path: url.path
        };
    }

    function groupingRuleKind(rule) {
        var constructorName = rule && rule.constructor && typeof rule.constructor.name === 'string' ? rule.constructor.name : '';
        if (rule && rule.media && typeof rule.media.mediaText === 'string') {
            return 'media';
        }
        if (constructorName === 'CSSMediaRule') { return 'media'; }
        if (constructorName === 'CSSSupportsRule') { return 'supports'; }
        if (constructorName === 'CSSContainerRule') { return 'container'; }
        if (constructorName === 'CSSScopeRule') { return 'scope'; }
        if (constructorName === 'CSSStartingStyleRule') { return 'starting-style'; }
        if (constructorName === 'CSSDocumentRule' || constructorName === 'CSSMozDocumentRule') { return 'document'; }
        if (constructorName === 'CSSLayerBlockRule') { return 'layer'; }
        if (constructorName === 'CSSKeyframesRule' || constructorName === 'WebKitCSSKeyframesRule') { return 'non-selector-group'; }
        return 'unknown-group';
    }

    function groupingConditionText(rule, kind) {
        var text = '';
        if (kind === 'media' && rule && rule.media && typeof rule.media.mediaText === 'string') {
            text = rule.media.mediaText;
        } else if (rule && typeof rule.conditionText === 'string') {
            text = rule.conditionText;
        }
        text = String(text || '').trim();
        return {
            text: text.slice(0, 2048),
            length: text.length
        };
    }

    function evaluateGroupingApplicability(rule, view) {
        var kind = groupingRuleKind(rule);
        var condition = groupingConditionText(rule, kind);
        var state = 'UNKNOWN';
        var record = true;

        if (kind === 'layer') {
            return { kind: kind, state: 'UNCONDITIONAL', conditionText: null, conditionLength: 0, record: false };
        }
        if (kind === 'non-selector-group') {
            return { kind: kind, state: 'SKIP', conditionText: null, conditionLength: 0, record: false };
        }
        if (kind === 'media' && condition.text && view && typeof view.matchMedia === 'function') {
            try {
                var mediaResult = view.matchMedia(condition.text);
                if (mediaResult && typeof mediaResult.matches === 'boolean') {
                    state = mediaResult.matches ? 'ACTIVE' : 'INACTIVE';
                }
            } catch (error) {
                state = 'UNKNOWN';
            }
        } else if (kind === 'supports' && condition.text && view && view.CSS && typeof view.CSS.supports === 'function') {
            try {
                var supportsResult = view.CSS.supports(condition.text);
                if (typeof supportsResult === 'boolean') {
                    state = supportsResult ? 'ACTIVE' : 'INACTIVE';
                }
            } catch (error) {
                state = 'UNKNOWN';
            }
        }

        return {
            kind: kind,
            state: state,
            conditionText: condition.text || null,
            conditionLength: condition.length,
            record: record
        };
    }

    function collectMatchedCascade(element, documentObject, view) {
        var result = {
            matchedRules: [],
            inaccessibleStylesheets: [],
            conditionalContexts: [],
            conditionalContextEvidenceTruncated: false,
            resolvedCustomProperties: fixedCustomProperties(element, view, SUBMIT_LOCAL_PROPERTIES),
            visitedRules: 0
        };
        if (!documentObject || !documentObject.styleSheets || !element || typeof element.matches !== 'function') {
            return result;
        }
        var sheets = bounded(documentObject.styleSheets, BUDGETS.stylesheetLinks);

        function recordContext(applicability, meta, sourceOrder) {
            if (!applicability.record) {
                return;
            }
            if (result.conditionalContexts.length >= BUDGETS.conditionalContexts) {
                result.conditionalContextEvidenceTruncated = true;
                return;
            }
            result.conditionalContexts.push({
                kind: applicability.kind,
                state: applicability.state,
                conditionText: applicability.conditionText,
                conditionLength: applicability.conditionLength,
                stylesheet: meta,
                sourceOrder: sourceOrder
            });
        }

        function visitRules(rules, meta, activeContexts) {
            if (!rules || result.visitedRules >= BUDGETS.cssRuleVisits || result.matchedRules.length >= BUDGETS.matchedCascadeRules) {
                return;
            }
            activeContexts = activeContexts || [];
            for (var r = 0; r < rules.length && result.visitedRules < BUDGETS.cssRuleVisits && result.matchedRules.length < BUDGETS.matchedCascadeRules; r += 1) {
                var rule = rules[r];
                result.visitedRules += 1;
                if (rule && rule.cssRules) {
                    var applicability = evaluateGroupingApplicability(rule, view);
                    recordContext(applicability, meta, result.visitedRules);
                    if (applicability.state === 'INACTIVE' || applicability.state === 'UNKNOWN' || applicability.state === 'SKIP') {
                        continue;
                    }
                    var nextContexts = activeContexts;
                    if (applicability.state === 'ACTIVE') {
                        if (activeContexts.length >= BUDGETS.groupingContextDepth) {
                            recordContext({
                                kind: 'grouping-context-depth-limit',
                                state: 'UNKNOWN',
                                conditionText: null,
                                conditionLength: 0,
                                record: true
                            }, meta, result.visitedRules);
                            continue;
                        }
                        nextContexts = activeContexts.concat([{
                            kind: applicability.kind,
                            state: 'ACTIVE',
                            conditionText: applicability.conditionText,
                            conditionLength: applicability.conditionLength,
                            sourceOrder: result.visitedRules
                        }]);
                    }
                    visitRules(rule.cssRules, meta, nextContexts);
                    continue;
                }
                if (!rule || typeof rule.selectorText !== 'string' || !rule.style) {
                    continue;
                }
                var declarations = {};
                for (var p = 0; p < SUBMIT_CASCADE_PROPERTIES.length; p += 1) {
                    var property = SUBMIT_CASCADE_PROPERTIES[p];
                    var declared = String(rule.style.getPropertyValue(property) || '').trim();
                    if (declared) {
                        declarations[property] = { declared: declared, priority: String(rule.style.getPropertyPriority(property) || '') };
                    }
                }
                if (!Object.keys(declarations).length) {
                    continue;
                }
                var branches = splitSelectorList(rule.selectorText);
                for (var b = 0; b < branches.length; b += 1) {
                    var branch = branches[b];
                    var matches = false;
                    try { matches = element.matches(branch); } catch (error) { matches = false; }
                    if (matches) {
                        result.matchedRules.push({
                            selectorBranch: branch.slice(0, 2048),
                            selectorLength: branch.length,
                            declarations: declarations,
                            stylesheet: meta,
                            sourceOrder: result.visitedRules,
                            applicabilityContext: activeContexts.slice()
                        });
                        if (result.matchedRules.length >= BUDGETS.matchedCascadeRules) { return; }
                    }
                }
            }
        }
        for (var s = 0; s < sheets.length && result.visitedRules < BUDGETS.cssRuleVisits; s += 1) {
            var sheet = sheets[s], rules;
            var meta = stylesheetMeta(sheet, s, documentObject);
            try { rules = sheet.cssRules; } catch (error) {
                result.inaccessibleStylesheets.push(meta);
                continue;
            }
            visitRules(rules, meta, []);
        }
        return result;
    }

    function collectSubmitLayout(target, documentObject, view) {
        return boundedQuery(target, 'button[type="submit"].gform_button, input[type="submit"].gform_button', BUDGETS.submitControls).map(function (submit) {
            var footer = typeof submit.closest === 'function' ? submit.closest('.gform-footer, .gform_footer') : null;
            var ancestors = [], cursor = submit.parentElement, depth = 0;
            while (cursor && depth < BUDGETS.submitAncestorDepth) {
                ancestors.push(elementSnapshot(cursor, view));
                if (cursor === target) { break; }
                cursor = cursor.parentElement; depth += 1;
            }
            return {
                submit: elementSnapshot(submit, view),
                footer: footer ? elementSnapshot(footer, view) : null,
                ancestors: ancestors,
                matchedCascade: collectMatchedCascade(submit, documentObject, view)
            };
        });
    }

    function collectUnrelatedForms(documentObject, view) {
        var all = boundedQuery(documentObject, '.gform_wrapper', BUDGETS.unrelatedForms + BUDGETS.targets);
        return all.filter(function (wrapper) {
            return !(wrapper.classList && wrapper.classList.contains('srwf-registration-theme_wrapper'));
        }).slice(0, BUDGETS.unrelatedForms).map(function (wrapper) {
            return elementSnapshot(wrapper, view);
        });
    }

    function safeCollect(failures, name, collector, fallback) {
        try {
            return collector();
        } catch (error) {
            failures.push({ collector: name, state: 'COLLECTOR_FAILED' });
            return fallback;
        }
    }

    function finalizeQualification(view, report) {
        if (!report || typeof report !== 'object') {
            return report;
        }
        if (!Array.isArray(report.collectorFailures)) {
            report.collectorFailures = [];
        }
        if (Object.prototype.hasOwnProperty.call(report, 'srwfV1Qualification')) {
            delete report.srwfV1Qualification;
        }

        var collector = view && view.GTB_SRWF_COLLECT_V1_QUALIFICATION_V034;
        try {
            if (typeof collector !== 'function') {
                throw new Error('v0.3.4 qualification collector unavailable');
            }
            var qualification = collector();
            if (!qualification || typeof qualification !== 'object' || Array.isArray(qualification)) {
                throw new Error('v0.3.4 qualification collector returned invalid payload');
            }
            report.srwfV1Qualification = qualification;
        } catch (error) {
            if (view) {
                view.GTB_SRWF_V1_QUALIFICATION_V034 = null;
            }
            report.collectorFailures.push({ collector: 'srwfV1Qualification', state: 'COLLECTOR_FAILED' });
        }
        return report;
    }

    function collectConsumers(target, documentObject, view, failures) {
        failures = failures || [];
        return {
            normalControls: safeCollect(failures, 'normalControls', function () { return collectNormalControls(target, view); }, []),
            submitControls: safeCollect(failures, 'submitControls', function () { return collectSubmitControls(target, view); }, []),
            submitLayout: safeCollect(failures, 'submitLayout', function () { return collectSubmitLayout(target, documentObject, view); }, []),
            validationAndFocus: safeCollect(failures, 'validationAndFocus', function () { return collectValidation(target, documentObject, view); }, { states: [], focusOwner: null }),
            enhancedSelects: safeCollect(failures, 'enhancedSelects', function () { return collectEnhancedSelects(target, view); }, []),
            uploads: safeCollect(failures, 'uploads', function () { return collectUploads(target, view); }, []),
            fileUploadProConsumer: safeCollect(failures, 'fileUploadProConsumer', function () { return collectGpfup(target, view); }, { state: 'COLLECTOR_FAILED', roots: [] }),
            titleConsumers: safeCollect(failures, 'titleConsumers', function () { return boundedQuery(target, '.gform_title', BUDGETS.titleConsumers).map(function (element) { return elementSnapshot(element, view); }); }, []),
            sectionConsumers: safeCollect(failures, 'sectionConsumers', function () { return boundedQuery(target, '.gfield--type-section .gsection_title', BUDGETS.sectionConsumers).map(function (element) { return elementSnapshot(element, view); }); }, []),
            fieldSignatures: safeCollect(failures, 'fieldSignatures', function () { return collectFieldSignatures(target); }, []),
            persianGravityConsumer: { state: 'NOT_PROVEN' }
        };
    }

    function run(documentObject, view) {
        var failures = [];
        var stylesheets = safeCollect(failures, 'stylesheetOrder', function () { return collectStylesheetOrder(documentObject); }, []);
        var targets = safeCollect(failures, 'targets', function () { return boundedQuery(documentObject, TARGET_SELECTOR, BUDGETS.targets); }, []);
        var unrelated = safeCollect(failures, 'unrelatedForms', function () { return collectUnrelatedForms(documentObject, view); }, []);
        return {
            schemaVersion: SCHEMA_VERSION,
            diagnosticVersion: DIAGNOSTIC_VERSION,
            diagnosticMode: 'admin-gated-read-only',
            budgets: BUDGETS,
            stylesheetOrder: stylesheets,
            unrelatedForms: unrelated,
            targets: targets.map(function (target, index) {
                var form = null;
                if (typeof target.querySelector === 'function') {
                    form = target.querySelector('form.srwf-registration-theme, form');
                }
                return {
                    targetIndex: index,
                    wrapper: elementSnapshot(target, view),
                    form: form ? elementSnapshot(form, view) : null,
                    canonicalProperties: safeCollect(failures, 'canonicalProperties.' + index, function () { return canonicalProperties(target, view); }, {}),
                    consumers: collectConsumers(target, documentObject, view, failures)
                };
            }),
            collectorFailures: failures
        };
    }

    function ensureDownloadControl(documentObject) {
        if (!documentObject || typeof documentObject.createElement !== 'function') {
            return null;
        }
        var existing = typeof documentObject.getElementById === 'function' ? documentObject.getElementById(DOWNLOAD_CONTROL_ID) : null;
        if (existing) {
            return existing;
        }
        var button = documentObject.createElement('button');
        button.id = DOWNLOAD_CONTROL_ID;
        button.type = 'button';
        button.setAttribute('aria-label', 'دانلود گزارش GTB');
        if (typeof documentObject.createTextNode === 'function') {
            button.appendChild(documentObject.createTextNode('دانلود گزارش GTB'));
        }
        button.style.position = 'fixed';
        button.style.left = '12px';
        button.style.bottom = '12px';
        button.style.zIndex = '2147483646';
        button.style.minHeight = '36px';
        button.style.padding = '8px 12px';
        button.style.border = '0';
        button.style.borderRadius = '6px';
        button.style.background = '#172033';
        button.style.color = '#FFFFFF';
        button.style.font = '600 13px Vazirmatn, system-ui, sans-serif';
        button.style.cursor = 'pointer';
        var parent = documentObject.body || documentObject.documentElement;
        if (parent && typeof parent.appendChild === 'function') {
            parent.appendChild(button);
        }
        return button;
    }

    function downloadJson(documentObject, view, report) {
        if (!documentObject || !view || typeof view.Blob !== 'function' || !view.URL || typeof view.URL.createObjectURL !== 'function') {
            return false;
        }
        var blob = new view.Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
        var url = view.URL.createObjectURL(blob);
        var anchor = documentObject.createElement('a');
        anchor.href = url;
        anchor.download = 'gtb-srwf-runtime-diagnostic-v0.3.0.json';
        if (typeof anchor.click === 'function') {
            anchor.click();
        }
        if (typeof view.URL.revokeObjectURL === 'function') {
            view.setTimeout(function () { view.URL.revokeObjectURL(url); }, 0);
        }
        return true;
    }

    return {
        SCHEMA_VERSION: SCHEMA_VERSION,
        DIAGNOSTIC_VERSION: DIAGNOSTIC_VERSION,
        BUDGETS: BUDGETS,
        TARGET_SELECTOR: TARGET_SELECTOR,
        selectSnapshot: selectSnapshot,
        collectNormalControls: collectNormalControls,
        collectEnhancedSelects: collectEnhancedSelects,
        collectGpfup: collectGpfup,
        collectConsumers: collectConsumers,
        collectMatchedCascade: collectMatchedCascade,
        shallowStructure: shallowStructure,
        splitSelectorList: splitSelectorList,
        ensureDownloadControl: ensureDownloadControl,
        downloadJson: downloadJson,
        finalizeQualification: finalizeQualification,
        run: run
    };
}));
