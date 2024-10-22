from burp import IBurpExtender, IHttpListener
from java.net import URL

class BurpExtender(IBurpExtender, IHttpListener):
    
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        
        # Set the name of the extension
        callbacks.setExtensionName("Send request to localhost for non-localhost requests")
        
        # Register this extension as an HTTP Listener
        callbacks.registerHttpListener(self)
        
        # Print message to alert tab
        callbacks.issueAlert("Burp Extension Initialized")
        print("Burp Extension Initialized")
    
    # This method is called for every HTTP request/response handled by Burp Suite
    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        # If it's a request, we will capture and process it
        if messageIsRequest:
            # Get the HTTP service (which contains host, port, and protocol info)
            http_service = messageInfo.getHttpService()
            
            # Get the host of the request
            host = http_service.getHost()
            
            # Check if the host is localhost (ignore if it's localhost or 127.0.0.1)
            if host == "localhost" or host == "127.0.0.1":
                return  # Ignore requests made to localhost
            
            # Send an additional request to localhost:5000
            self.send_request_to_localhost(messageInfo.getRequest())
    
    def send_request_to_localhost(self, http_request):
        try:
            # Create the URL object for localhost
            url = URL("http://localhost:5000/")
            
            # Build a new request to localhost:5000
            http_service = self._helpers.buildHttpService(url.getHost(), url.getPort(), url.getProtocol())
            request = self._helpers.buildHttpRequest(url)
            
            # Send the request using Burp's HTTP client
            response = self._callbacks.makeHttpRequest(http_service, request)
            
            # Parse the response
            response_info = self._helpers.analyzeResponse(response.getResponse())
            response_body = response.getResponse()[response_info.getBodyOffset():].tostring()
            
            # Log the response status code and body
            print("Response from localhost:5000 - Status Code: {}".format(response_info.getStatusCode()))
            print("Response Body: {}".format(response_body))
        
        except Exception as e:
            print("Failed to send request to localhost:5000: {}".format(e))

