'use strict';

goog.provide('Blockly.JavaScript.conditions');

goog.require('Blockly.JavaScript');

Blockly.JavaScript['if_else'] = function(block) {
  var value_name = Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_condicion = Blockly.JavaScript.statementToCode(block, 'condicion');
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};
