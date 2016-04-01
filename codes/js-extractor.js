# eval-finder.py Utility
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com

var webPage= require('webpage')
var system = require('system')

if (system.args.length === 1) {
	console.log('Usage: js-extractor.js <html file>');
	phantom.exit();
}

var html = system.args[1];
var page = webPage.create();

page.onConsoleMessage = function(msg) {
	console.log(msg);
};

page.onInitialized = function () {
	page.evaluate(function () {
		window.eval = function(arg) { 
			console.log("[*] eval() Detected:", arg);
		};	
	});
};

page.open(html, function(status) {
	phantom.exit();
});

