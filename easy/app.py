from modulefinder import IMPORT_NAME
import os
import sys
import typing as t

import os
import sys
import typing as t

from werkzeug.routing import Map
from werkzeug.routing import Rule
from werkzeug.wrappers import Request
from werkzeug.wrappers import Response
from werkzeug.exceptions import HTTPException

class Easy:
    def __init__(self,name) -> None:
        self.url_map = Map()
        self.view_funcs = {}
        self.root_path = self.get_root_path(name)
        
    def get_root_path(self, name:str) -> str:
        mod = sys.modules.get(name)
        if mod and hasattr(mod, '__file__') and mod.__file__:
            return os.path.dirname(os.path.abspath(mod.__file__))
        else:
            return os.getcwd()
        
    def add_url_rule(self,rule:str,endpoint:t.Optional[str] = None, view_func:t.Callable = None, methods: t.Tuple[str] = None, **options:t.Any) -> None:
        rule = Rule(rule,methods=methods,endpoint=endpoint, **options)
        self.url_map.add(rule)

        func_exists = self.view_funcs.get(endpoint)
        if func_exists and func_exists != view_func:
            raise Exception(f"overwriting the previous endpoint:{endpoint}")
        self.view_funcs[endpoint] = view_func
        
    
    def route(self, rule: str, endpoint: t.Optional[str] = None, methods: t.Tuple[str] = None, **options: t.Any) -> None:
        def decorator(f):
            self.add_url_rule(rule,endpoint,f,methods,**options)
            return f
        return decorator
    
    def run(self, host: t.Optional[str] = None, port: t.Optional[int] = None, debug: t.Optional[bool] = True, **options: t.Any) -> t.Any:
        server_name = os.environ.get("SERVER_NAME")
        sn_host = sn_port = None
        if server_name:
            sn_host, _, sn_port = server_name.partition(":")

        if not host:
            if sn_host:
                host = sn_host
            else:
                host = "127.0.0.1"

        if port or port == 0:
            port = int(port)
        elif sn_port:
            port = int(sn_port)
        else:
            port = 5000

        from werkzeug.serving import run_simple

        run_simple(host, port, self, **options)
    def dispatch_request(self, request: Request) -> Response:
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            view_function = self.view_funcs[endpoint]
            rv = view_function(request, **values)
        except HTTPException as e:
            return e

        return Response(rv)
    def wsgi_app(self, environ: dict, start_response: t.Callable) -> Response:
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)
    
    def __call__(self, environ: dict, start_response: t.Callable) -> t.Any:
        
                return self.wsgi_app(environ, start_response)

