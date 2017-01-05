
AU_STATES = {
  "TAS": "Tasmania",
  "ACT": "Australian Capital Territory",
  "NSW": "New South Wales",
  "NT": "Northern Territory",
  "QLD": "Queensland",
  "VIC": "Victoria",
  "SA": "South Australia",
  "WA": "Western Australia",
}

function profile_form() {
  selects = $("select");
  for (var i=0; i<selects.length; i++) {
    select = selects[i];
    id = select.id;
    if (!id.endsWith("country")) {
      continue;
    }
    parts = id.split("-");
    _id = parts[parts.length - 1];
    prefix = parts.slice(0, parts.length - 1).join("-");

    mutate_state(select, prefix);
    $(select).change(function() { mutate_state(select, prefix) })
  }
}

function mutate_state(country_select, prefix) {
  id = prefix + "-state";
  var $state = $("#" + id);
  var $select = $(country_select);
  var $parent = $state.parent();
  state = $state.val();
  state_field_name = $state.attr("name");
  country = $select.val()

  $state.remove();

  console.log($parent);
  if (country == "AU") {
    $p = $("<select>");

    $p.append($("<option>").attr({
      "value": "",
    }).text("Select a state..."));
    for (var state_key in AU_STATES) {
      $opt = $("<option>").attr({
        "value": state_key,
      });
      $opt.text(AU_STATES[state_key]);
      $p.append($opt);
    }
    $parent.attr("class", "form-field select");
  } else {
    // state textfield
    $p = $("<input>").attr({
      "type": "text",
      "maxlength": 256,
    });
    $parent.attr("class", "form-field");
  }
  $p.attr({
    "id": id,
    "name": state_field_name,
  });
  $p.val(state);
  $parent.append($p);
}

function __defer_profile_form() {
  if (window.jQuery) {
    profile_form();
  } else {
    setTimeout(__defer_profile_form(), 50);
  }
}
__defer_profile_form();
