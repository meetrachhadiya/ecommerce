class DemoMiddleWare:
    def __init__(self, get_response):
        print('DemoMiddleware init')
        print(get_response)
        # print(dir(get_response))
        # print(get_response.__str__)
        self.get_response = get_response
        self.exeption_count = 0

    def __call__(self, request):
        print("Start DemoMiddleware call")
        print("Before Call process_view")

        response = self.get_response(request)

        print("After Call process_view")
        print("Response is :", response)
        print(response.status_code)
        print("End DemoMiddleware call")
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        print("Start DemoMiddleware process_view")  
        print("view_func:", view_func)
        print(view_args)
        print(view_kwargs)  
        # print(dir(view_func))
        print("view_func name : ",view_func.__name__)
        print("End DemoMiddleware process_view")

    def process_exception(self, request, exception):
        print("DemoMiddleware process_exception")
        print(exception)
        self.exeption_count += 1
        print("Exception Count : ", self.exeption_count)
        

    
    