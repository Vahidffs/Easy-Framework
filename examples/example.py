from easy import Easy

app = Easy(__name__)

def test_url(request):
    return "hello world!"

app.add_url_rule("/test", "test_url", test_url)


def test_url_with_param(request, **values):
    return str(values)

app.add_url_rule("/test/<int:id>", "test_url_with_param", test_url_with_param)

@app.route("/test_decorator/<string:name>")
def test_decorator(request, name):
    return f"hello {name}"

app.run()