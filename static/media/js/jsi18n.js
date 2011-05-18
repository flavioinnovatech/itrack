/* gettext library */

var catalog = new Array();

function pluralidx(n) {
  var v=(n > 1);
  if (typeof(v) == 'boolean') {
    return v ? 1 : 0;
  } else {
    return v;
  }
}
catalog['%(sel)s of %(cnt)s selected'] = ['',''];
catalog['%(sel)s of %(cnt)s selected'][0] = '%(sel)s de %(cnt)s selecionado';
catalog['%(sel)s of %(cnt)s selected'][1] = '%(sel)s de %(cnt)s selecionados';
catalog['6 a.m.'] = '6 da manh\u00e3';
catalog['Add'] = 'Adicionar';
catalog['Available %s'] = '%s dispon\u00edveis';
catalog['Calendar'] = 'Calend\u00e1rio';
catalog['Cancel'] = 'Cancelar';
catalog['Choose a time'] = 'Escolha uma hora';
catalog['Choose all'] = 'Escolher todos';
catalog['Chosen %s'] = '%s escolhido(s)';
catalog['Clear all'] = 'Limpar tudo';
catalog['Clock'] = 'Rel\u00f3gio';
catalog['Filter'] = 'Filtro';
catalog['Hide'] = 'Esconder';
catalog['January February March April May June July August September October November December'] = 'Janeiro Fevereiro Mar\u00e7o Abril Maio Junho Julho Agosto Setembro Outubro Novembro Dezembro';
catalog['Midnight'] = 'Meia-noite';
catalog['Noon'] = 'Meio-dia';
catalog['Now'] = 'Agora';
catalog['Remove'] = 'Remover';
catalog['S M T W T F S'] = 'D S T Q Q S S';
catalog['Select your choice(s) and click '] = 'Selecione sua(s) escolha(s) e clique ';
catalog['Show'] = 'Mostrar';
catalog['Sunday Monday Tuesday Wednesday Thursday Friday Saturday'] = 'Domingo Segunda Ter\u00e7a Quarta Quinta Sexta S\u00e1bado';
catalog['Today'] = 'Hoje';
catalog['Tomorrow'] = 'Amanh\u00e3';
catalog['Yesterday'] = 'Ontem';
catalog['You have selected an action, and you haven\'t made any changes on individual fields. You\'re probably looking for the Go button rather than the Save button.'] = 'Voc\u00ea selecionou uma a\u00e7\u00e3o, e voc\u00ea n\u00e3o fez altera\u00e7\u00f5es em campos individuais. Voc\u00ea provavelmente est\u00e1 procurando o bot\u00e3o Ir ao inv\u00e9s do bot\u00e3o "Salvar".';
catalog['You have selected an action, but you haven\'t saved your changes to individual fields yet. Please click OK to save. You\'ll need to re-run the action.'] = 'Voc\u00ea selecionou uma a\u00e7\u00e3o, mas voc\u00ea n\u00e3o salvou as altera\u00e7\u00f5es de cada campo ainda. Clique em OK para salvar. Voc\u00ea vai precisar executar novamente a a\u00e7\u00e3o.';
catalog['You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost.'] = 'Voc\u00ea tem altera\u00e7\u00f5es n\u00e3o salvas em campos edit\u00e1veis individuais. Se voc\u00ea executar uma a\u00e7\u00e3o suas altera\u00e7\u00f5es n\u00e3o salvas ser\u00e3o perdidas.';


function gettext(msgid) {
  var value = catalog[msgid];
  if (typeof(value) == 'undefined') {
    return msgid;
  } else {
    return (typeof(value) == 'string') ? value : value[0];
  }
}

function ngettext(singular, plural, count) {
  value = catalog[singular];
  if (typeof(value) == 'undefined') {
    return (count == 1) ? singular : plural;
  } else {
    return value[pluralidx(count)];
  }
}

function gettext_noop(msgid) { return msgid; }

function pgettext(context, msgid) {
  var value = gettext(context + '' + msgid);
  if (value.indexOf('') != -1) {
    value = msgid;
  }
  return value;
}

function npgettext(context, singular, plural, count) {
  var value = ngettext(context + '' + singular, context + '' + plural, count);
  if (value.indexOf('') != -1) {
    value = ngettext(singular, plural, count);
  }
  return value;
}

function interpolate(fmt, obj, named) {
  if (named) {
    return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
  } else {
    return fmt.replace(/%s/g, function(match){return String(obj.shift())});
  }
}

/* formatting library */

var formats = new Array();

formats['DATETIME_FORMAT'] = 'j \\de N \\de Y \u00e0\\s H:i';
formats['DATE_FORMAT'] = 'j \\de N \\de Y';
formats['DECIMAL_SEPARATOR'] = ',';
formats['MONTH_DAY_FORMAT'] = 'j \\de F';
formats['NUMBER_GROUPING'] = '3';
formats['TIME_FORMAT'] = 'H:i';
formats['FIRST_DAY_OF_WEEK'] = '0';
formats['TIME_INPUT_FORMATS'] = ['%H:%M:%S', '%H:%M'];
formats['THOUSAND_SEPARATOR'] = '.';
formats['DATE_INPUT_FORMATS'] = ['%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y'];
formats['YEAR_MONTH_FORMAT'] = 'F \\de Y';
formats['SHORT_DATE_FORMAT'] = 'd/m/Y';
formats['SHORT_DATETIME_FORMAT'] = 'd/m/Y H:i';
formats['DATETIME_INPUT_FORMATS'] = ['%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%Y', '%d/%m/%y %H:%M:%S', '%d/%m/%y %H:%M', '%d/%m/%y', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d'];

function get_format(format_type) {
    var value = formats[format_type];
    if (typeof(value) == 'undefined') {
      return msgid;
    } else {
      return value;
    }
}
