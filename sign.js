const docusign = require('docusign-esign');

// create a byte array that will hold our document bytes
var fileBytes = null;

try {
	var fs = require('fs');
	var path = require('path');

	// read file from a local directory
	fileBytes = fs.readFileSync(path.resolve(__dirname, "test.pdf"));
}
catch (ex) {
	console.log('Exception: ' + ex);
}

// Create an envelope that will store the document(s), field(s), and recipient(s)
var envDef = new docusign.EnvelopeDefinition();
envDef.emailSubject = 'Confirm that this is your face.';

// add a document to the envelope
var doc = new docusign.Document();
var base64Doc = new Buffer(fileBytes).toString('base64');
doc.documentBase64 = base64Doc;
doc.name = 'FaceConfirmation.pdf';
doc.extention = 'pdf';
doc.documentId = '1';

var docs = [];
docs.push(doc);
envDef.documents = docs;

// add a recipient to sign the document, identified by name and email
var signer = new docusign.Signer();
signer.email = 'dfritsch99@gmail.com';
signer.name = 'John Doe';
signer.recipientId = '1';

//*** important: must set the clientUserId property to embed the recipient!
// otherwise DocuSign platform will treat recipient as remote and your
// integration will not be able to generate a signing token for the recipient
signer.clientUserId = '1001';

// Create a signhere tab 100 pixels down and 150 right from the top left
// corner of first page of document.
var signHere = new docusign.SignHere();
signHere.documentId = '1';
signHere.pageNumber = '1';
signHere.recipientId = '1';
signHere.xPosition = '100';
signHere.yPosition = '150';

// can have multiple tabs, so need to add to envelope as a single element list
var signHereTabs = [];
signHereTabs.push(signHere);
var tabs = new docusign.Tabs();
tabs.signHereTabs = signHereTabs;
signer.tabs = tabs;

// add recipients (in this case a single signer) to the envelope
envDef.recipients = new docusign.Recipients();
envDef.recipients.signers = [];
envDef.recipients.signers.push(signer);

// send the envelope by setting |status| to "sent". To save as a draft set to "created"
envDef.status = 'sent';

// instantiate a new EnvelopesApi object
var envelopesApi = new docusign.EnvelopesApi();

// call the createEnvelope() API to create and send the envelope
envelopesApi.createEnvelope(accountId, {'envelopeDefinition': envDef}, function (err, envelopeSummary, response) {
	if (err) {
	  return next(err);
	}
	console.log('EnvelopeSummary: ' + JSON.stringify(envelopeSummary));
});

// next we want to generate the signing link for the recipient...


// instantiate a new EnvelopesApi object
var envelopesApi = new docusign.EnvelopesApi();

// set the url where you want the recipient to go once they are done signing
// should typically be a callback route somewhere in your app
var viewRequest = new docusign.RecipientViewRequest();
viewRequest.returnUrl = 'http://danielfritsch.com';
viewRequest.authenticationMethod = 'email';

// recipient information must match embedded recipient info we provided
viewRequest.email = 'dfritsch99@gmail.com';
viewRequest.userName = 'John Doe';
viewRequest.recipientId = '1';
viewRequest.clientUserId = '1001';

// call the CreateRecipientView API
envelopesApi.createRecipientView(accountId, envelopeId, {'recipientViewRequest': viewRequest}, function (error, recipientView, response) {
	if (error) {
		console.log('Error: ' + error);
		return;
	}

	if (recipientView) {
		console.log('ViewUrl: ' + JSON.stringify(recipientView));
	}
	return JSON.stringify(recipientView);
});