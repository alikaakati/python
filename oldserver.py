from xmlrpc.server import SimpleXMLRPCServer
s = SimpleXMLRPCServer(("", 4242), logRequests=False) # Localhost at port 4242
def twice(x): # Example function
    print("received request from client")
    print(x)
    return x * 2
s.register_function(twice) # Add functionality to the server
print("running on port 4242")
s.serve_forever() # Start the server