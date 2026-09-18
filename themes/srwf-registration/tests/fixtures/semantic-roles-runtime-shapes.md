# SRWF semantic-role runtime-shape fixtures

These fixtures record only the structural classes needed by the static qualification suite. They intentionally omit user-entered values and labels as selector authority.

## Binary choice field

```html
<fieldset class="gfield gfield--type-radio gfield--type-choice gfield--input-type-radio srwf-role-binary-choice">
  <legend class="gfield_label gform-field-label gfield_label_before_complex"></legend>
  <div class="ginput_container ginput_container_radio">
    <div class="gfield_radio">
      <div class="gchoice">
        <input class="gfield-choice-input" type="radio" id="fixture_choice_a" name="fixture_choice" value="a">
        <label for="fixture_choice_a"></label>
      </div>
      <div class="gchoice">
        <input class="gfield-choice-input" type="radio" id="fixture_choice_b" name="fixture_choice" value="b" checked>
        <label for="fixture_choice_b"></label>
      </div>
    </div>
  </div>
</fieldset>
```

## Ordinary radio field

```html
<fieldset class="gfield gfield--type-radio gfield--type-choice gfield--input-type-radio gfield--choice-align-vertical">
  <div class="gfield_radio"><div class="gchoice"></div></div>
</fieldset>
```

## Report Card — initial GPFUP

```html
<div class="gfield gfield--type-fileupload gfield--input-type-fileupload srwf-role-report-card-upload">
  <div class="ginput_container ginput_container_fileupload">
    <div class="gform_fileupload_multifile">
      <div class="gpfup gpfup--strict gform-theme__no-reset--children">
        <div class="gpfup__droparea">
          <button class="gpfup__select-files gform_button_select_files" type="button"></button>
        </div>
      </div>
    </div>
    <span class="gfield_description gform_fileupload_rules"></span>
  </div>
</div>
```

## Report Card — authentic uploaded host state

```html
<div class="gfield gfield--type-fileupload gfield--input-type-fileupload srwf-role-report-card-upload">
  <div class="gpfup gpfup--strict gpfup--has-files gform-theme__no-reset--children">
    <div class="gpfup__files">
      <div class="gpfup__file">
        <button class="gpfup__delete" type="button"></button>
      </div>
    </div>
    <div class="gpfup__droparea">
      <button class="gpfup__select-files gform_button_select_files" type="button"></button>
    </div>
  </div>
</div>
```

## Student Photo — captured pre-upload host state

```html
<div class="gfield gfield--type-fileupload gfield--input-type-fileupload">
  <div class="gpfup gpfup--strict gpfup--images-only gform-theme__no-reset--children">
    <div class="gpfup__droparea"></div>
  </div>
</div>
```

## Section Break roles

```html
<div class="gfield gfield--type-section gsection srwf-role-section-identity"><h3 class="gsection_title"></h3></div>
<div class="gfield gfield--type-section gsection srwf-role-section-contact"><h3 class="gsection_title"></h3></div>
<div class="gfield gfield--type-section gsection srwf-role-section-education"><h3 class="gsection_title"></h3></div>
<div class="gfield gfield--type-section gsection srwf-role-section-school-documents"><h3 class="gsection_title"></h3></div>
<div class="gfield gfield--type-section gsection srwf-role-section-student-photo"><h3 class="gsection_title"></h3></div>
<div class="gfield gfield--type-section gsection"><h3 class="gsection_title"></h3></div>
```
